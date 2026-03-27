/* ============================================
   SCRIPT PRINCIPAL - DASHBOARD LACS
   ============================================ */

// Configuration
const API_URL = document.querySelector('script[src*="dashboard"]')?.dataset?.apiBase || '/api';

// État global
let currentTab = 'overview';
let isDarkMode = localStorage.getItem('dark-mode') === 'true';

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', () => {
    initializeDarkMode();
    setupEventListeners();
    loadInitialData();
    checkApiStatus();
    updateDate();
});

/* ============================================
   GESTION DU THÈME
   ============================================ */
function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    localStorage.setItem('dark-mode', isDarkMode);
    document.body.classList.toggle('dark-mode');
}

function initializeDarkMode() {
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
}

/* ============================================
   UTILITAIRES
   ============================================ */
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

function updateDate() {
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        dateEl.textContent = new Date().toLocaleDateString('fr-FR', options);
    }
}

function toggleForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.classList.toggle('hidden');
    }
}

async function fetchAPI(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || result.detail || 'Erreur API');
        }
        
        return result;
    } catch (error) {
        showToast('Erreur: ' + error.message);
        console.error(error);
        return null;
    }
}

/* ============================================
   GESTION DES ONGLETS
   ============================================ */
function setupEventListeners() {
    // Onglets
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tab = item.dataset.tab;
            if (tab) switchTab(tab);
        });
    });
}

function switchTab(tabName) {
    // Masquer tous les onglets
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.remove('active');
    });
    
    // Désactiver tous les nav items
    document.querySelectorAll('.nav-item').forEach(el => {
        el.classList.remove('active');
    });
    
    // Afficher le nouvel onglet
    const tabEl = document.getElementById(tabName + '-tab');
    if (tabEl) {
        tabEl.classList.add('active');
    }
    
    // Activer le nav item
    document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');
    
    // Mettre à jour le titre
    const titles = {
        'overview': 'Aperçu',
        'eleves': 'Gestion des Élèves',
        'classes': 'Gestion des Classes',
        'inscriptions': 'Gestion des Inscriptions',
        'formateurs': 'Formateurs',
        'matieres': 'Gestion des Matières',
        'evaluations': 'Gestion des Évaluations',
        'notes': 'Gestion des Notes',
        'api-test': 'Testeur API Générique'
    };
    
    const titleEl = document.getElementById('page-title');
    if (titleEl) {
        titleEl.textContent = titles[tabName] || 'Tab';
    }
    
    // Charger les données si nécessaire
    loadTabData(tabName);
    
    currentTab = tabName;
}

/* ============================================
   CHARGEMENT DES DONNÉES
   ============================================ */
async function loadInitialData() {
    await loadAnneesScolaires();
    await loadMatieres();
    loadOverviewStats();
}

async function loadTabData(tabName) {
    switch(tabName) {
        case 'eleves':
            await loadEleves();
            break;
        case 'classes':
            await loadClasses();
            break;
        case 'inscriptions':
            await loadInscriptions();
            await loadEleves();
            await loadClasses();
            break;
        case 'formateurs':
            await loadFormateurs();
            break;
        case 'evaluations':
            await loadEvaluations();
            await loadMatieres();
            await loadClasses();
            await loadAnneesScolaires();
            break;
        case 'notes':
            await loadAnneesScolaires();
            await loadEleves();
            await loadEvaluations();
            break;
    }
}

async function checkApiStatus() {
    const response = await fetch('/api/health');
    const result = await response.json();
    const statusEl = document.getElementById('api-status');
    
    if (statusEl) {
        if (result.api_status === 'online') {
            statusEl.innerHTML = `
                <div class="alert alert-success">
                    <strong>API En ligne ✓</strong><br>
                    <code>${result.api_url}</code>
                </div>
            `;
        } else {
            statusEl.innerHTML = `
                <div class="alert alert-error">
                    <strong>API Hors ligne ✗</strong><br>
                    <code>${result.api_url}</code>
                </div>
            `;
        }
    }
}

async function loadAnneesScolaires() {
    try {
        const data = await fetchAPI('/api/annees-scolaires');
        if (data && data.data) {
            const annees = data.data;
            
            // Remplir tous les selects
            ['classe-annee_scolaire_id', 'inscription-annee_scolaire_id', 'evaluation-annee_scolaire_id', 'note-annee_scolaire_id'].forEach(id => {
                const select = document.getElementById(id);
                if (select) {
                    select.innerHTML = '<option value="">-- Sélectionner --</option>';
                    annees.forEach(annee => {
                        const opt = document.createElement('option');
                        opt.value = annee.id;
                        opt.textContent = annee.name + (annee.is_active ? ' (actif)' : '');
                        select.appendChild(opt);
                    });
                }
            });
        }
    } catch (error) {
        console.error('Erreur lors du chargement des années:', error);
    }
}

async function loadEleves() {
    try {
        const data = await fetchAPI('/api/eleves');
        if (data && data.data) {
            const elevesDiv = document.getElementById('eleves-list');
            if (elevesDiv) {
                if (data.data.length === 0) {
                    elevesDiv.innerHTML = '<p class="text-muted">Aucun élève.</p>';
                } else {
                    elevesDiv.innerHTML = data.data.map(eleve => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">${eleve.name} ${eleve.firstname}</div>
                                <div class="list-item-meta">
                                    <strong>Email:</strong> ${eleve.email} | 
                                    <strong>Matricule:</strong> ${eleve.matricule}
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
            }
            
            // Remplir le select des élèves
            const select = document.getElementById('inscription-eleve_id');
            if (select) {
                select.innerHTML = '<option value="">-- Sélectionner --</option>';
                data.data.forEach(eleve => {
                    const opt = document.createElement('option');
                    opt.value = eleve.id;
                    opt.textContent = `${eleve.name} ${eleve.firstname} (${eleve.matricule})`;
                    select.appendChild(opt);
                });
            }
            
            const selectNote = document.getElementById('note-eleve_id');
            if (selectNote) {
                selectNote.innerHTML = '<option value="">-- Sélectionner --</option>';
                data.data.forEach(eleve => {
                    const opt = document.createElement('option');
                    opt.value = eleve.id;
                    opt.textContent = `${eleve.name} ${eleve.firstname}`;
                    selectNote.appendChild(opt);
                });
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des élèves:', error);
    }
}

async function loadClasses() {
    try {
        const data = await fetchAPI('/api/classes');
        if (data && data.data) {
            const classesDiv = document.getElementById('classes-list');
            if (classesDiv) {
                if (data.data.length === 0) {
                    classesDiv.innerHTML = '<p class="text-muted">Aucune classe.</p>';
                } else {
                    classesDiv.innerHTML = data.data.map(classe => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">${classe.name}</div>
                                <div class="list-item-meta">
                                    <strong>ID:</strong> ${classe.id}
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
            }
            
            // Remplir les selects
            const selectInsc = document.getElementById('inscription-classe_id');
            if (selectInsc) {
                selectInsc.innerHTML = '<option value="">-- Sélectionner --</option>';
                data.data.forEach(classe => {
                    const opt = document.createElement('option');
                    opt.value = classe.id;
                    opt.textContent = classe.name;
                    selectInsc.appendChild(opt);
                });
            }
            
            const selectEval = document.getElementById('evaluation-classe_id');
            if (selectEval) {
                selectEval.innerHTML = '<option value="">-- Sélectionner --</option>';
                data.data.forEach(classe => {
                    const opt = document.createElement('option');
                    opt.value = classe.id;
                    opt.textContent = classe.name;
                    selectEval.appendChild(opt);
                });
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des classes:', error);
    }
}

async function loadInscriptions() {
    try {
        const data = await fetchAPI('/api/inscriptions');
        if (data && data.data) {
            const inscDiv = document.getElementById('inscriptions-list');
            if (inscDiv) {
                if (data.data.length === 0) {
                    inscDiv.innerHTML = '<p class="text-muted">Aucune inscription.</p>';
                } else {
                    inscDiv.innerHTML = data.data.map(insc => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">Inscription #${insc.id.substring(0, 8)}</div>
                                <div class="list-item-meta">
                                    <strong>Élève:</strong> ${insc.eleve_id} | 
                                    <strong>Classe:</strong> ${insc.classe_id} | 
                                    <strong>Année:</strong> ${insc.annee_scolaire_id}
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des inscriptions:', error);
    }
}

async function loadFormateurs() {
    try {
        const data = await fetchAPI('/api/formateurs');
        if (data && data.data) {
            const formatDiv = document.getElementById('formateurs-list');
            if (formatDiv) {
                if (data.data.length === 0) {
                    formatDiv.innerHTML = '<p class="text-muted">Aucun formateur.</p>';
                } else {
                    formatDiv.innerHTML = data.data.map(form => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">Formateur #${form.id.substring(0, 8)}</div>
                                <div class="list-item-meta">
                                    <strong>ID Utilisateur:</strong> ${form.user_id.substring(0, 8)}
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des formateurs:', error);
    }
}

async function loadMatieres() {
    try {
        const data = await fetchAPI('/api/matieres');
        if (data && data.data) {
            const matieres = data.data;
            
            // Remplir le select des matières
            const selectEval = document.getElementById('evaluation-matiere_id');
            if (selectEval) {
                selectEval.innerHTML = '<option value="">-- Sélectionner --</option>';
                matieres.forEach(mat => {
                    const opt = document.createElement('option');
                    opt.value = mat.id;
                    opt.textContent = mat.name;
                    selectEval.appendChild(opt);
                });
            }
            
            // Afficher la liste
            const matDiv = document.getElementById('matieres-list');
            if (matDiv) {
                if (matieres.length === 0) {
                    matDiv.innerHTML = '<p class="text-muted">Aucune matière.</p>';
                } else {
                    matDiv.innerHTML = matieres.map(mat => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">${mat.name}</div>
                                <div class="list-item-meta"><strong>ID:</strong> ${mat.id.substring(0, 8)}</div>
                            </div>
                        </div>
                    `).join('');
                }
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des matières:', error);
    }
}

async function loadEvaluations() {
    try {
        const data = await fetchAPI('/api/evaluations');
        if (data && data.data) {
            const evalDiv = document.getElementById('evaluations-list');
            if (evalDiv) {
                if (data.data.length === 0) {
                    evalDiv.innerHTML = '<p class="text-muted">Aucune évaluation.</p>';
                } else {
                    evalDiv.innerHTML = data.data.map(evaluation => `
                        <div class="list-item">
                            <div class="list-item-content">
                                <div class="list-item-title">${evaluation.titre}</div>
                                <div class="list-item-meta">
                                    <strong>Barème:</strong> ${evaluation.bareme} | 
                                    <strong>Date:</strong> ${new Date(evaluation.date).toLocaleDateString('fr-FR')}
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
            }
            
            // Remplir le select des évaluations
            const selectNote = document.getElementById('note-evaluation_id');
            if (selectNote) {
                selectNote.innerHTML = '<option value="">-- Sélectionner --</option>';
                data.data.forEach(evaluation => {
                    const opt = document.createElement('option');
                    opt.value = evaluation.id;
                    opt.textContent = evaluation.titre;
                    selectNote.appendChild(opt);
                });
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des évaluations:', error);
    }
}

async function loadOverviewStats() {
    try {
        const elevesData = await fetchAPI('/api/eleves?limit=1');
        const classesData = await fetchAPI('/api/classes?limit=1');
        const formateursData = await fetchAPI('/api/formateurs?limit=1');
        
        if (elevesData?.data) {
            const countEl = document.getElementById('stat-eleves');
            if (countEl) countEl.textContent = elevesData.data.length;
        }
        
        if (classesData?.data) {
            const countEl = document.getElementById('stat-classes');
            if (countEl) countEl.textContent = classesData.data.length;
        }
        
        if (formateursData?.data) {
            const countEl = document.getElementById('stat-formateurs');
            if (countEl) countEl.textContent = formateursData.data.length;
        }
    } catch (error) {
        console.error('Erreur lors du chargement des stats:', error);
    }
}

/* ============================================
   FONCTIONS DE CRÉATION (CRUD)
   ============================================ */
async function createEleve() {
    const name = document.getElementById('eleve-name').value;
    const firstname = document.getElementById('eleve-firstname').value;
    const email = document.getElementById('eleve-email').value;
    const password = document.getElementById('eleve-password').value;
    
    if (!name || !firstname || !email || !password) {
        showToast('Tous les champs sont obligatoires');
        return;
    }
    
    const data = {
        name,
        firstname,
        email,
        password,
        matricule: `LACS-${new Date().getFullYear()}-AUTO`
    };
    
    const result = await fetchAPI('/api/create-eleve', 'POST', data);
    if (result) {
        showToast('Élève créé avec succès!');
        document.getElementById('eleve-form').reset();
        document.getElementById('eleve-form').classList.add('hidden');
        loadEleves();
    }
}

async function createClasse() {
    const name = document.getElementById('classe-name').value;
    const annee_scolaire_id = document.getElementById('classe-annee_scolaire_id').value;
    
    if (!name || !annee_scolaire_id) {
        showToast('Tous les champs sont obligatoires');
        return;
    }
    
    const data = { name, annee_scolaire_id };
    const result = await fetchAPI('/api/create-classe', 'POST', data);
    if (result) {
        showToast('Classe créée avec succès!');
        document.getElementById('classe-form').reset();
        document.getElementById('classe-form').classList.add('hidden');
        loadClasses();
    }
}

async function createInscription() {
    const eleve_id = document.getElementById('inscription-eleve_id').value;
    const classe_id = document.getElementById('inscription-classe_id').value;
    const annee_scolaire_id = document.getElementById('inscription-annee_scolaire_id').value;
    const is_ancien = document.getElementById('inscription-is_ancien').checked;
    
    if (!eleve_id || !classe_id || !annee_scolaire_id) {
        showToast('Tous les  champs sont obligatoires');
        return;
    }
    
    const data = {
        eleve_id,
        classe_id,
        annee_scolaire_id,
        is_ancien
    };
    
    const result = await fetchAPI('/api/create-inscription', 'POST', data);
    if (result) {
        showToast('Inscription créée avec succès!');
        document.getElementById('inscription-form').reset();
        document.getElementById('inscription-form').classList.add('hidden');
        loadInscriptions();
    }
}

async function createMatiere() {
    const name = document.getElementById('matiere-name').value;
    
    if (!name) {
        showToast('Le nom est obligatoire');
        return;
    }
    
    const data = { name };
    const result = await fetchAPI('/api/create-matiere', 'POST', data);
    if (result) {
        showToast('Matière créée avec succès!');
        document.getElementById('matiere-form').reset();
        document.getElementById('matiere-form').classList.add('hidden');
        loadMatieres();
    }
}

async function createEvaluation() {
    const titre = document.getElementById('evaluation-titre').value;
    const matiere_id = document.getElementById('evaluation-matiere_id').value;
    const classe_id = document.getElementById('evaluation-classe_id').value;
    const annee_scolaire_id = document.getElementById('evaluation-annee_scolaire_id').value;
    const date = document.getElementById('evaluation-date').value;
    const bareme = document.getElementById('evaluation-bareme').value || 20;
    
    if (!titre || !matiere_id || !classe_id || !annee_scolaire_id) {
        showToast('Les champs obligatoires ne sont pas remplis');
        return;
    }
    
    const data = {
        titre,
        matiere_id,
        classe_id,
        annee_scolaire_id,
        date: date ? new Date(date).toISOString() : null,
        bareme: parseInt(bareme)
    };
    
    const result = await fetchAPI('/api/create-evaluation', 'POST', data);
    if (result) {
        showToast('Évaluation créée avec succès!');
        document.getElementById('evaluation-form').reset();
        document.getElementById('evaluation-form').classList.add('hidden');
        loadEvaluations();
    }
}

async function createNote() {
    const eleve_id = document.getElementById('note-eleve_id').value;
    const evaluation_id = document.getElementById('note-evaluation_id').value;
    const valeur = document.getElementById('note-valeur').value;
    const commentaire = document.getElementById('note-commentaire').value;
    
    if (!eleve_id || !evaluation_id || !valeur) {
        showToast('Les champs obligatoires ne sont pas remplis');
        return;
    }
    
    const data = {
        eleve_id,
        evaluation_id,
        valeur: parseFloat(valeur),
        commentaire
    };
    
    const result = await fetchAPI('/api/create-note', 'POST', data);
    if (result) {
        showToast('Note créée avec succès!');
        document.getElementById('note-form').reset();
        document.getElementById('note-form').classList.add('hidden');
        loadTabData('notes');
    }
}

/* ============================================
   TESTEUR API GÉNÉRIQUE
   ============================================ */
function setApiMethod(method) {
    currentApiMethod = method;
    document.querySelectorAll('.button-group .btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-secondary');
    });
    event.target.classList.add('btn-primary');
    event.target.classList.remove('btn-secondary');
}

async function testApi() {
    const endpoint = document.getElementById('api-endpoint').value;
    const payload = document.getElementById('api-payload').value;
    const responseBox = document.getElementById('api-response');
    const responseContent = document.getElementById('api-response-content');
    
    if (!endpoint) {
        showToast('Veuillez entrer un endpoint');
        return;
    }
    
    let data = null;
    if (['POST', 'PUT', 'PATCH'].includes(currentApiMethod) && payload) {
        try {
            data = JSON.parse(payload);
        } catch {
            showToast('Payload JSON invalide');
            return;
        }
    }
    
    const url = `/api/proxy?endpoint=${encodeURIComponent(endpoint)}`;
    
    try {
        const response = await fetch(url, {
            method: currentApiMethod,
            headers: { 'Content-Type': 'application/json' },
            body: data ? JSON.stringify(data) : undefined
        });
        
        const result = await response.json();
        responseContent.textContent = JSON.stringify(result, null, 2);
        responseBox.classList.remove('hidden');
        showToast('Requête envoyée!');
    } catch (error) {
        responseContent.textContent = 'Erreur: ' + error.message;
        responseBox.classList.remove('hidden');
    }
}
