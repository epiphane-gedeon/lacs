// Inscription Form Handler
class InscriptionForm {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.formData = {};
        this.prices = {
            'Mathématiques': 200,
            'Physique-Chimie': 180,
            'SVT': 180,
            'Méthodologie': 120,
            'inscription': 85
        };

        this.init();
    }

    init() {
        this.populateFormData();
        this.bindEvents();
        this.updateProgressBar();
        this.updatePriceSummary();
    }

    populateFormData() {
        // Populate form fields that are missing in HTML
        this.populatePersonalInfoFields();
        this.populateAcademicFields();
        this.populateCourseFields();
    }

    populatePersonalInfoFields() {
        const step1 = document.getElementById('step1');
        const formRows = step1.querySelectorAll('.form-row .form-group');

        // First row - Name fields
        formRows[0].innerHTML = `
            <label for="firstName" class="form-label">Prénom <span class="required">*</span></label>
            <input type="text" id="firstName" name="firstName" class="form-input" required>
            <div class="error-text" id="firstNameError"></div>
        `;

        formRows[1].innerHTML = `
            <label for="lastName" class="form-label">Nom <span class="required">*</span></label>
            <input type="text" id="lastName" name="lastName" class="form-input" required>
            <div class="error-text" id="lastNameError"></div>
        `;

        // Second row - Contact info
        formRows[2].innerHTML = `
            <label for="email" class="form-label">Email <span class="required">*</span></label>
            <input type="email" id="email" name="email" class="form-input" required>
            <div class="error-text" id="emailError"></div>
        `;

        formRows[3].innerHTML = `
            <label for="phone" class="form-label">Téléphone <span class="required">*</span></label>
            <input type="tel" id="phone" name="phone" class="form-input" required>
            <div class="error-text" id="phoneError"></div>
        `;

        // Third row - Birth info
        formRows[4].innerHTML = `
            <label for="birthDate" class="form-label">Date de naissance <span class="required">*</span></label>
            <input type="date" id="birthDate" name="birthDate" class="form-input" required>
            <div class="error-text" id="birthDateError"></div>
        `;

        formRows[5].innerHTML = `
            <label for="gender" class="form-label">Genre <span class="required">*</span></label>
            <select id="gender" name="gender" class="form-input form-select" required>
                <option value="">Choisir</option>
                <option value="male">Masculin</option>
                <option value="female">Féminin</option>
            </select>
            <div class="error-text" id="genderError"></div>
        `;

        // Parent name label
        const parentNameGroup = step1.querySelectorAll('.form-row')[3].querySelector('.form-group');
        parentNameGroup.innerHTML = `
            <label for="parentName" class="form-label">Nom du responsable <span class="required">*</span></label>
            <input type="text" id="parentName" name="parentName" class="form-input" required>
            <div class="error-text" id="parentNameError"></div>
        `;
    }

    populateAcademicFields() {
        // Current level select
        const currentLevelSelect = document.getElementById('currentLevel');
        currentLevelSelect.innerHTML = `
            <option value="">Choisir votre niveau</option>
            <option value="3eme">3ème</option>
            <option value="2nde">2nde</option>
            <option value="1ere">1ère</option>
            <option value="terminale">Terminale</option>
            <option value="bac1">Bac+1</option>
            <option value="bac2">Bac+2</option>
        `;

        // Math level select
        const mathLevelSelect = document.getElementById('mathLevel');
        mathLevelSelect.innerHTML = `
            <option value="">Évaluer votre niveau</option>
            <option value="excellent">Excellent (16-20/20)</option>
            <option value="bon">Bon (14-16/20)</option>
            <option value="moyen">Moyen (12-14/20)</option>
            <option value="faible">Faible (10-12/20)</option>
            <option value="difficile">Difficultés (< 10/20)</option>
        `;

        // Specialties checkboxes
        const checkboxGroup = document.querySelector('#step2 .checkbox-group');
        checkboxGroup.innerHTML = `
            <div class="checkbox-item">
                <input type="checkbox" id="specMath" name="specialties" value="Mathématiques">
                <label for="specMath">Mathématiques</label>
            </div>
            <div class="checkbox-item">
                <input type="checkbox" id="specPhysics" name="specialties" value="Physique-Chimie">
                <label for="specPhysics">Physique-Chimie</label>
            </div>
            <div class="checkbox-item">
                <input type="checkbox" id="specSVT" name="specialties" value="SVT">
                <label for="specSVT">Sciences de la Vie et de la Terre</label>
            </div>
            <div class="checkbox-item">
                <input type="checkbox" id="specHGGSP" name="specialties" value="HGGSP">
                <label for="specHGGSP">Histoire-Géographie</label>
            </div>
            <div class="checkbox-item">
                <input type="checkbox" id="specSES" name="specialties" value="SES">
                <label for="specSES">Sciences Économiques</label>
            </div>
        `;

        // File upload text
        const fileText = document.querySelector('.file-text');
        fileText.innerHTML = `
            <strong>Glissez vos documents ici</strong><br>
            <small>ou cliquez pour parcourir</small><br>
            <small>Bulletins, relevés de notes (PDF, JPG, PNG)</small>
        `;
    }

    populateCourseFields() {
        // Program radio buttons
        const programRadios = document.querySelectorAll('#step3 .radio-item label');
        programRadios[0].innerHTML = `
            <strong>Programme Standard</strong><br>
            <small>Cours de soutien - 200€/mois</small>
        `;
        programRadios[1].innerHTML = `
            <strong>Programme Intensif</strong><br>
            <small>Perfectionnement - 350€/mois</small>
        `;
        programRadios[2].innerHTML = `
            <strong>Programme Excellence</strong><br>
            <small>Préparation concours - 500€/mois</small>
        `;

        // Subject checkboxes
        const subjectLabels = document.querySelectorAll('#step3 .checkbox-item label');
        subjectLabels[0].innerHTML = `
            <strong>Mathématiques</strong><br>
            <small>200€/mois - 4h/semaine</small>
        `;
        subjectLabels[1].innerHTML = `
            <strong>Physique-Chimie</strong><br>
            <small>180€/mois - 3h/semaine</small>
        `;
    }

    bindEvents() {
        // Navigation buttons
        document.getElementById('nextBtn').addEventListener('click', () => this.nextStep());
        document.getElementById('prevBtn').addEventListener('click', () => this.prevStep());

        // Form validation on input
        document.querySelectorAll('.form-input').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });

        // Checkbox and radio interactions
        document.addEventListener('click', (e) => {
            const item = e.target.closest('.checkbox-item, .radio-item');
            if (item) {
                e.preventDefault(); // Empêche le double-clic sur l'input

                const input = item.querySelector('input');
                if (input) {
                    if (input.type === 'radio') {
                        // Pour les boutons radio
                        document.querySelectorAll(`input[name="${input.name}"]`).forEach(radio => {
                            radio.closest('.radio-item').classList.remove('selected');
                            radio.checked = false;
                        });
                        input.checked = true;
                        item.classList.add('selected');
                    } else if (input.type === 'checkbox') {
                        // Pour les cases à cocher
                        input.checked = !input.checked;
                        item.classList.toggle('selected', input.checked);
                    }
                    this.updatePriceSummary();
                }
            }
        });

        // Subject selection for price calculation
        document.querySelectorAll('input[name="subjects"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => this.updatePriceSummary());
        });

        // Payment method selection
        document.querySelectorAll('.payment-method').forEach(method => {
            method.addEventListener('click', () => {
                document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('selected'));
                method.classList.add('selected');
                this.clearError(document.getElementById('paymentError'));
            });
        });

        // File upload handling
        document.getElementById('documents').addEventListener('change', (e) => {
            const files = e.target.files;
            const fileName = document.getElementById('fileName');
            if (files.length > 0) {
                fileName.textContent = `${files.length} fichier(s) sélectionné(s)`;
                fileName.style.display = 'block';
            }
        });

        // Terms checkbox
        document.getElementById('terms').addEventListener('change', (e) => {
            if (e.target.checked) {
                this.clearError(document.getElementById('termsError'));
            }
        });
    }

    nextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.showStep(this.currentStep);
                this.updateProgressBar();

                if (this.currentStep === 4) {
                    this.populateSummary();
                }
            } else {
                this.submitForm();
            }
        }
    }

    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.showStep(this.currentStep);
            this.updateProgressBar();
        }
    }

    showStep(step) {
        // Hide all steps
        document.querySelectorAll('.form-step').forEach(s => {
            s.classList.remove('active');
        });

        // Show current step
        document.getElementById(`step${step}`).classList.add('active');

        // Update navigation buttons
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const btnText = nextBtn.querySelector('.btn-text');

        prevBtn.style.display = step > 1 ? 'flex' : 'none';

        if (step === this.totalSteps) {
            btnText.textContent = 'Confirmer l\'inscription';
            nextBtn.querySelector('i').className = 'fas fa-check';
        } else {
            btnText.textContent = 'Suivant';
            nextBtn.querySelector('i').className = 'fas fa-arrow-right';
        }
    }

    updateProgressBar() {
        const steps = document.querySelectorAll('.step');
        const progressLine = document.getElementById('progressLine');

        steps.forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');

            if (stepNum < this.currentStep) {
                step.classList.add('completed');
                step.querySelector('.step-circle').innerHTML = '<i class="fas fa-check"></i>';
            } else if (stepNum === this.currentStep) {
                step.classList.add('active');
                step.querySelector('.step-circle').textContent = stepNum;
            } else {
                step.querySelector('.step-circle').textContent = stepNum;
            }
        });

        // Update progress line
        const progressPercentage = ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
        progressLine.style.width = `${progressPercentage}%`;
    }

    updatePriceSummary() {
        const selectedSubjects = document.querySelectorAll('input[name="subjects"]:checked');
        const selectedSubjectsCount = document.getElementById('selectedSubjectsCount');
        const totalPrice = document.getElementById('totalPrice');

        let monthlyTotal = 0;
        selectedSubjects.forEach(subject => {
            monthlyTotal += this.prices[subject.value] || 0;
        });

        const totalWithInscription = monthlyTotal + this.prices.inscription;

        if (selectedSubjectsCount) {
            selectedSubjectsCount.textContent = selectedSubjects.length;
        }
        if (totalPrice) {
            totalPrice.textContent = `${totalWithInscription}€`;
        }
    }

    validateCurrentStep() {
        let isValid = true;
        const currentStepElement = document.getElementById(`step${this.currentStep}`);
        const requiredFields = currentStepElement.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        // Special validations
        if (this.currentStep === 3) {
            // Check if at least one subject is selected
            const selectedSubjects = document.querySelectorAll('input[name="subjects"]:checked');
            if (selectedSubjects.length === 0) {
                this.showError('subjectsError', 'Veuillez sélectionner au moins une matière');
                isValid = false;
            }

            // Check if program is selected
            const selectedProgram = document.querySelector('input[name="program"]:checked');
            if (!selectedProgram) {
                this.showError('programError', 'Veuillez sélectionner un programme');
                isValid = false;
            }
        }

        if (this.currentStep === 4) {
            // Check payment method
            const selectedPayment = document.querySelector('.payment-method.selected');
            if (!selectedPayment) {
                this.showError('paymentError', 'Veuillez sélectionner un mode de paiement');
                isValid = false;
            }

            // Check terms acceptance
            const terms = document.getElementById('terms');
            if (!terms.checked) {
                this.showError('termsError', 'Vous devez accepter les conditions générales');
                isValid = false;
            }
        }

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            errorMessage = 'Ce champ est obligatoire';
            isValid = false;
        }

        // Specific field validations
        if (value && isValid) {
            switch (fieldName) {
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        errorMessage = 'Format d\'email invalide';
                        isValid = false;
                    }
                    break;
                case 'phone':
                case 'parentPhone':
                    const phoneRegex = /^[0-9\s\-\+\(\)]{10,}$/;
                    if (!phoneRegex.test(value)) {
                        errorMessage = 'Format de téléphone invalide';
                        isValid = false;
                    }
                    break;
                case 'birthDate':
                    const birthDate = new Date(value);
                    const today = new Date();
                    const age = today.getFullYear() - birthDate.getFullYear();
                    if (age < 12 || age > 25) {
                        errorMessage = 'L\'âge doit être entre 12 et 25 ans';
                        isValid = false;
                    }
                    break;
            }
        }

        if (isValid) {
            this.clearError(field);
            field.classList.remove('error');
            field.classList.add('success');
        } else {
            this.showError(`${fieldName}Error`, errorMessage);
            field.classList.remove('success');
            field.classList.add('error');
        }

        return isValid;
    }

    showError(errorElementId, message) {
        const errorElement = document.getElementById(errorElementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
    }

    clearError(field) {
        if (typeof field === 'string') {
            const errorElement = document.getElementById(field);
            if (errorElement) {
                errorElement.classList.remove('show');
            }
        } else {
            const errorElement = document.getElementById(`${field.name}Error`);
            if (errorElement) {
                errorElement.classList.remove('show');
            }
        }
    }

    populateSummary() {
        // Personal info summary
        document.getElementById('summaryName').textContent =
            `${document.getElementById('firstName').value} ${document.getElementById('lastName').value}`;
        document.getElementById('summaryEmail').textContent =
            document.getElementById('email').value;
        document.getElementById('summaryPhone').textContent =
            document.getElementById('phone').value;
        document.getElementById('summaryParent').textContent =
            document.getElementById('parentName').value;

        // Academic info summary
        const levelSelect = document.getElementById('currentLevel');
        document.getElementById('summaryLevel').textContent =
            levelSelect.options[levelSelect.selectedIndex].text;
        document.getElementById('summarySchool').textContent =
            document.getElementById('currentSchool').value;

        const mathSelect = document.getElementById('mathLevel');
        document.getElementById('summaryMathLevel').textContent =
            mathSelect.options[mathSelect.selectedIndex].text;

        const scienceSelect = document.getElementById('scienceLevel');
        document.getElementById('summaryScienceLevel').textContent =
            scienceSelect.options[scienceSelect.selectedIndex].text;

        // Course info summary
        const selectedProgram = document.querySelector('input[name="program"]:checked');
        document.getElementById('summaryProgram').textContent =
            selectedProgram ? selectedProgram.nextElementSibling.querySelector('strong').textContent : '-';

        const selectedSubjects = Array.from(document.querySelectorAll('input[name="subjects"]:checked'))
            .map(cb => cb.value).join(', ');
        document.getElementById('summarySubjects').textContent = selectedSubjects || '-';

        const startSelect = document.getElementById('startDate');
        document.getElementById('summaryStartDate').textContent =
            startSelect.options[startSelect.selectedIndex].text;

        const scheduleSelect = document.getElementById('schedule');
        document.getElementById('summarySchedule').textContent =
            scheduleSelect.options[scheduleSelect.selectedIndex].text;

        // Price summary
        const selectedSubjectElements = document.querySelectorAll('input[name="subjects"]:checked');
        let monthlyTotal = 0;
        selectedSubjectElements.forEach(subject => {
            monthlyTotal += this.prices[subject.value] || 0;
        });

        document.getElementById('summaryMonthlyPrice').textContent = `${monthlyTotal}€`;
        document.getElementById('summaryTotalPrice').textContent = `${monthlyTotal + this.prices.inscription}€`;
    }

    async submitForm() {
        const nextBtn = document.getElementById('nextBtn');
        const spinner = nextBtn.querySelector('.loading-spinner');
        const btnText = nextBtn.querySelector('.btn-text');

        // Show loading state
        nextBtn.classList.add('loading');
        nextBtn.disabled = true;
        btnText.textContent = 'Traitement en cours...';

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Generate reference number
            const referenceNumber = `LACS-2025-${String(Math.floor(Math.random() * 9999) + 1).padStart(4, '0')}`;
            document.getElementById('referenceNumber').textContent = referenceNumber;

            // Show success step
            document.querySelectorAll('.form-step').forEach(step => step.classList.remove('active'));
            document.getElementById('stepSuccess').classList.add('active');
            document.getElementById('navigationButtons').style.display = 'none';

            // Send confirmation email (simulation)
            this.sendConfirmationEmail();

        } catch (error) {
            console.error('Erreur lors de la soumission:', error);
            this.showMessage('step4Message', 'Une erreur est survenue. Veuillez réessayer.', 'error');
        } finally {
            nextBtn.classList.remove('loading');
            nextBtn.disabled = false;
            btnText.textContent = 'Confirmer l\'inscription';
        }
    }

    sendConfirmationEmail() {
        // Simulation of email sending
        console.log('Email de confirmation envoyé');

        // You would integrate with your email service here
        // Example: EmailJS, Nodemailer, or your backend API
    }

    showMessage(containerId, message, type) {
        const messageContainer = document.getElementById(containerId);
        messageContainer.textContent = message;
        messageContainer.className = `message ${type} show`;

        setTimeout(() => {
            messageContainer.classList.remove('show');
        }, 5000);
    }
}

// Initialize the form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new InscriptionForm();
});

// Newsletter form handler
document.getElementById('newsletterForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = e.target.querySelector('.newsletter-input').value;

    // Simulate newsletter subscription
    console.log('Newsletter subscription:', email);
    alert('Merci pour votre inscription à la newsletter !');
    e.target.reset();
});
