"""
Application Flask pour tester l'API LACS
- Proxy vers API FastAPI
- Gestion sessions JWT
- Interface complète de testing
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import os
from datetime import datetime, timezone
from functools import wraps

app = Flask(__name__)
app.secret_key = "test-secret-key-lacs-2026"

# Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_ENDPOINTS = {
    "auth_login": f"{API_BASE_URL}/auth/login",
    "auth_me": f"{API_BASE_URL}/auth/me",
    "eleves": f"{API_BASE_URL}/eleves",
    "classes": f"{API_BASE_URL}/classes",
    "inscriptions": f"{API_BASE_URL}/inscriptions",
    "annees_scolaires": f"{API_BASE_URL}/annees-scolaires",
    "formateurs": f"{API_BASE_URL}/formateurs",
    "matieres": f"{API_BASE_URL}/matieres",
    "parents": f"{API_BASE_URL}/parents",
    "evaluations": f"{API_BASE_URL}/evaluations",
    "notes": f"{API_BASE_URL}/notes",
    "absences": f"{API_BASE_URL}/absences",
}

def require_login(f):
    """Décorateur pour vérifier la présence d'un JWT"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_headers():
    """Obtenir les headers d'authentification"""
    token = session.get('access_token')
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    } if token else {}

def api_call(method, endpoint_name, endpoint_override=None, **kwargs):
    """Wrapper pour appels API"""
    try:
        url = endpoint_override or API_ENDPOINTS.get(endpoint_name)
        if not url:
            return {"error": f"Endpoint '{endpoint_name}' not found"}, 400
        
        response = requests.request(
            method,
            url,
            headers=get_headers(),
            timeout=10,
            **kwargs
        )
        
        result = {
            'status_code': response.status_code,
            'data': response.json() if response.text else None,
        }
        return result, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# ===== ROUTES PUBLIQUES =====

@app.route('/')
def index():
    """Redirection vers login ou dashboard"""
    if 'access_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        result, status = api_call('POST', 'auth_login', None,
            data={'username': email, 'password': password}
        )
        
        if status == 200 and 'access_token' in (result.get('data') or {}):
            session['access_token'] = result['data']['access_token']
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        else:
            error = result.get('data', {}).get('detail', 'Erreur de connexion')
            return render_template('login.html', error=error, email=email)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Déconnexion"""
    session.clear()
    return redirect(url_for('login'))

# ===== ROUTES PROTÉGÉES =====

@app.route('/dashboard')
@require_login
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html', 
        user_email=session.get('user_email'),
        api_base=API_BASE_URL
    )

@app.route('/api/eleves')
@require_login
def get_eleves():
    """Récupérer les élèves paginés"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'eleves', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

@app.route('/api/classes')
@require_login
def get_classes():
    """Récupérer les classes"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'classes', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

@app.route('/api/annees-scolaires')
@require_login
def get_annees():
    """Récupérer les années scolaires"""
    result, status = api_call('GET', 'annees_scolaires', None, params={})
    return jsonify(result), status

@app.route('/api/inscriptions')
@require_login
def get_inscriptions():
    """Récupérer les inscriptions"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'inscriptions', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

@app.route('/api/formateurs')
@require_login
def get_formateurs():
    """Récupérer les formateurs"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'formateurs', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

@app.route('/api/matieres')
@require_login
def get_matieres():
    """Récupérer les matières"""
    result, status = api_call('GET', 'matieres', None, params={})
    return jsonify(result), status

@app.route('/api/evaluations')
@require_login
def get_evaluations():
    """Récupérer les évaluations"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'evaluations', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

@app.route('/api/parents')
@require_login
def get_parents():
    """Récupérer les parents"""
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    result, status = api_call('GET', 'parents', None,
        params={'skip': skip, 'limit': limit}
    )
    return jsonify(result), status

# ===== ENDPOINTS PROXY POUR TESTING =====

@app.route('/api/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@require_login
def proxy_request():
    """Proxy générique pour tester n'importe quel endpoint"""
    endpoint = request.args.get('endpoint', '')
    method = request.method
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        kwargs = {}
        if method in ['POST', 'PUT', 'PATCH']:
            kwargs['json'] = request.get_json()
        else:
            kwargs['params'] = request.args.to_dict()
        
        response = requests.request(
            method, url,
            headers=get_headers(),
            timeout=10,
            **kwargs
        )
        
        return jsonify({
            'status_code': response.status_code,
            'data': response.json() if response.text else None,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-eleve', methods=['POST'])
@require_login
def create_eleve():
    """Créer un élève via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'eleves', None, json=data)
    return jsonify(result), status

@app.route('/api/create-classe', methods=['POST'])
@require_login
def create_classe():
    """Créer une classe via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'classes', None, json=data)
    return jsonify(result), status

@app.route('/api/create-inscription', methods=['POST'])
@require_login
def create_inscription():
    """Créer une inscription via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'inscriptions', None, json=data)
    return jsonify(result), status

@app.route('/api/create-matiere', methods=['POST'])
@require_login
def create_matiere():
    """Créer une matière via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'matieres', None, json=data)
    return jsonify(result), status

@app.route('/api/create-evaluation', methods=['POST'])
@require_login
def create_evaluation():
    """Créer une évaluation via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'evaluations', None, json=data)
    return jsonify(result), status

@app.route('/api/create-note', methods=['POST'])
@require_login
def create_note():
    """Créer une note via l'API"""
    data = request.get_json()
    result, status = api_call('POST', 'notes', None, json=data)
    return jsonify(result), status

@app.route('/api/health')
def health():
    """Vérifier que l'API est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        return jsonify({
            'status': 'ok',
            'api_url': API_BASE_URL,
            'api_status': 'online' if response.status_code == 200 else 'offline'
        })
    except:
        return jsonify({
            'status': 'error',
            'api_url': API_BASE_URL,
            'api_status': 'offline'
        }), 503

if __name__ == '__main__':
    app.run(debug=True, port=5000)
