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
        // formRows[0].innerHTML = `
        //     <label for="firstName" class="form-label">Prénom <span class="required">*</span></label>
        //     <input type="text" id="firstName" name="firstName" class="form-input" required>
        //     <div class="error-text" id="firstNameError"></div>
        // `;

        // formRows[1].innerHTML = `
        //     <label for="lastName" class="form-label">Nom <span class="required">*</span></label>
        //     <input type="text" id="lastName" name="lastName" class="form-input" required>
        //     <div class="error-text" id="lastNameError"></div>
        // `;

        // // Second row - Contact info
        // formRows[2].innerHTML = `
        //     <label for="email" class="form-label">Email <span class="required">*</span></label>
        //     <input type="email" id="email" name="email" class="form-input" required>
        //     <div class="error-text" id="emailError"></div>
        // `;

        // formRows[3].innerHTML = `
        //     <label for="phone" class="form-label">Téléphone <span class="required">*</span></label>
        //     <input type="tel" id="phone" name="phone" class="form-input" required>
        //     <div class="error-text" id="phoneError"></div>
        // `;

        // // Third row - Birth info
        // formRows[4].innerHTML = `
        //     <label for="birthDate" class="form-label">Date de naissance <span class="required">*</span></label>
        //     <input type="date" id="birthDate" name="birthDate" class="form-input" required>
        //     <div class="error-text" id="birthDateError"></div>
        // `;

        // formRows[5].innerHTML = `
        //     <label for="gender" class="form-label">Genre <span class="required">*</span></label>
        //     <select id="gender" name="gender" class="form-input form-select" required>
        //         <option value="">Choisir</option>
        //         <option value="male">Masculin</option>
        //         <option value="female">Féminin</option>
        //     </select>
        //     <div class="error-text" id="genderError"></div>
        // `;

        // // Parent name label
        // const parentNameGroup = step1.querySelectorAll('.form-row')[3].querySelector('.form-group');
        // parentNameGroup.innerHTML = `
        //     <label for="parentName" class="form-label">Nom du responsable <span class="required">*</span></label>
        //     <input type="text" id="parentName" name="parentName" class="form-input" required>
        //     <div class="error-text" id="parentNameError"></div>
        // `;
    }

    populateAcademicFields() {
        // Current level select
        // const currentLevelSelect = document.getElementById('currentLevel');
        // currentLevelSelect.innerHTML = `
        //     <option value="">Choisir votre niveau</option>
        //     <option value="3eme">3ème</option>
        //     <option value="2nde">2nde</option>
        //     <option value="1ere">1ère</option>
        //     <option value="terminale">Terminale</option>
        //     <option value="bac1">Bac+1</option>
        //     <option value="bac2">Bac+2</option>
        // `;

        // // Math level select
        // const mathLevelSelect = document.getElementById('mathLevel');
        // mathLevelSelect.innerHTML = `
        //     <option value="">Évaluer votre niveau</option>
        //     <option value="excellent">Excellent (16-20/20)</option>
        //     <option value="bon">Bon (14-16/20)</option>
        //     <option value="moyen">Moyen (12-14/20)</option>
        //     <option value="faible">Faible (10-12/20)</option>
        //     <option value="difficile">Difficultés (< 10/20)</option>
        // `;

        // // Specialties checkboxes
        // const checkboxGroup = document.querySelector('#step2 .checkbox-group');
        // checkboxGroup.innerHTML = `
        //     <div class="checkbox-item">
        //         <input type="checkbox" id="specMath" name="specialties" value="Mathématiques">
        //         <label for="specMath">Mathématiques</label>
        //     </div>
        //     <div class="checkbox-item">
        //         <input type="checkbox" id="specPhysics" name="specialties" value="Physique-Chimie">
        //         <label for="specPhysics">Physique-Chimie</label>
        //     </div>
        //     <div class="checkbox-item">
        //         <input type="checkbox" id="specSVT" name="specialties" value="SVT">
        //         <label for="specSVT">Sciences de la Vie et de la Terre</label>
        //     </div>
        //     <div class="checkbox-item">
        //         <input type="checkbox" id="specHGGSP" name="specialties" value="HGGSP">
        //         <label for="specHGGSP">Histoire-Géographie</label>
        //     </div>
        //     <div class="checkbox-item">
        //         <input type="checkbox" id="specSES" name="specialties" value="SES">
        //         <label for="specSES">Sciences Économiques</label>
        //     </div>
        // `;

        // // File upload text
        // const fileText = document.querySelector('.file-text');
        // fileText.innerHTML = `
        //     <strong>Glissez vos documents ici</strong><br>
        //     <small>ou cliquez pour parcourir</small><br>
        //     <small>Bulletins, relevés de notes (PDF, JPG, PNG)</small>
        // `;
    }

    populateCourseFields() {
        // // Program radio buttons
        // const programRadios = document.querySelectorAll('#step3 .radio-item label');
        // programRadios[0].innerHTML = `
        //     <strong>Programme Standard</strong><br>
        //     <small>Cours de soutien - 200€/mois</small>
        // `;
        // programRadios[1].innerHTML = `
        //     <strong>Programme Intensif</strong><br>
        //     <small>Perfectionnement - 350€/mois</small>
        // `;
        // programRadios[2].innerHTML = `
        //     <strong>Programme Excellence</strong><br>
        //     <small>Préparation concours - 500€/mois</small>
        // `;

        // // Subject checkboxes
        // const subjectLabels = document.querySelectorAll('#step3 .checkbox-item label');
        // subjectLabels[0].innerHTML = `
        //     <strong>Mathématiques</strong><br>
        //     <small>200€/mois - 4h/semaine</small>
        // `;
        // subjectLabels[1].innerHTML = `
        //     <strong>Physique-Chimie</strong><br>
        //     <small>180€/mois - 3h/semaine</small>
        // `;
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
        // document.querySelectorAll('input[name="subjects"]').forEach(checkbox => {
        //     checkbox.addEventListener('change', () => this.updatePriceSummary());
        // });

        // // Payment method selection
        // document.querySelectorAll('.payment-method').forEach(method => {
        //     method.addEventListener('click', () => {
        //         document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('selected'));
        //         method.classList.add('selected');
        //         this.clearError(document.getElementById('paymentError'));
        //     });
        // });

        // File upload handling
        document.getElementById('bulletin').addEventListener('change', (e) => {
            const files = e.target.files;
            const fileName = document.getElementById('fileName');
            if (files.length > 0) {
                fileName.textContent = `${files.length} fichier(s) sélectionné(s)`;
                fileName.style.display = 'block';
            }
        });

        // Gestion dynamique du champ série selon le niveau d'étude
        const niveauEtudeSelect = document.getElementById('niveau_etude');
        const seriesContainer = document.querySelector('input[name="series"]').closest('.form-group');
        const seriesInputs = document.querySelectorAll('input[name="series"]');

        if (niveauEtudeSelect && seriesContainer) {
            // Fonction pour mettre à jour la visibilité et l'obligation de la série
            const updateSeriesRequirement = () => {
                const niveau = niveauEtudeSelect.value;
                const isPremiereOrTerminale = niveau === 'premiere' || niveau === 'terminale';

                if (isPremiereOrTerminale) {
                    // Afficher la série
                    seriesContainer.style.display = 'block';

                    // Décocher l'option vide cachée pour forcer une sélection
                    const emptyOption = document.querySelector('input[name="series"][value=""]');
                    if (emptyOption) {
                        emptyOption.checked = false;
                    }

                    // Mettre à jour le label pour indiquer que c'est obligatoire
                    const label = seriesContainer.querySelector('label');
                    if (label && !label.querySelector('.required')) {
                        label.innerHTML += ' <span class="required">*</span>';
                    }
                } else {
                    // Cacher la série
                    seriesContainer.style.display = 'none';
                    seriesInputs.forEach(input => {
                        input.checked = false; // Décocher toutes les séries
                    });

                    // Recocher l'option vide pour les autres niveaux
                    const emptyOption = document.querySelector('input[name="series"][value=""]');
                    if (emptyOption) {
                        emptyOption.checked = true;
                    }

                    // Retirer l'astérisque obligatoire du label
                    const label = seriesContainer.querySelector('label');
                    const requiredSpan = label?.querySelector('.required');
                    if (requiredSpan) {
                        requiredSpan.remove();
                    }

                    // Effacer les erreurs de validation sur les séries
                    this.clearError(document.getElementById('seriesError') || 'seriesError');
                }
            };

            // Appliquer au chargement de la page
            updateSeriesRequirement();

            // Écouter les changements de niveau d'étude
            niveauEtudeSelect.addEventListener('change', updateSeriesRequirement);
        }

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
            }
            // Ne plus appeler submitForm() ici, le bouton submit s'en chargera
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
        const submitButton = document.getElementById('submitButton');
        const btnText = nextBtn.querySelector('.btn-text');

        prevBtn.style.display = step > 1 ? 'flex' : 'none';

        if (step === this.totalSteps) {
            // À la dernière étape, cacher le bouton Next et afficher le bouton Submit Flask
            nextBtn.style.display = 'none';
            submitButton.style.display = 'block';
        } else {
            // Aux autres étapes, afficher le bouton Next et cacher le bouton Submit
            nextBtn.style.display = 'flex';
            submitButton.style.display = 'none';
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

        // Valider uniquement les champs avec required qui sont visibles et pertinents
        const requiredFields = currentStepElement.querySelectorAll('input[required], select[required], textarea[required]');

        requiredFields.forEach(field => {
            // Ignorer les champs cachés ou dans des conteneurs cachés
            const fieldContainer = field.closest('.form-group');
            const isVisible = fieldContainer && window.getComputedStyle(fieldContainer).display !== 'none';

            // Ignorer aussi les radio buttons non cochés sauf s'il n'y en a aucun de coché
            if (field.type === 'radio') {
                const radioGroup = document.querySelectorAll(`input[name="${field.name}"]`);
                const hasChecked = Array.from(radioGroup).some(radio => radio.checked);

                // Pour les radios, on valide seulement s'il n'y en a aucun de coché
                if (!hasChecked && isVisible) {
                    if (!this.validateField(field)) {
                        isValid = false;
                    }
                }
            } else if (isVisible) {
                // Pour les autres types de champs
                if (!this.validateField(field)) {
                    isValid = false;
                }
            }
        });

        // Special validations
        if (this.currentStep === 2) {
            // Validation spéciale pour la série si Première ou Terminale est sélectionné
            const niveauEtude = document.getElementById('niveau_etude').value;
            console.log('Niveau d\'étude:', niveauEtude);

            if (niveauEtude === 'premiere' || niveauEtude === 'terminale') {
                // Chercher une série sélectionnée qui n'est pas l'option vide cachée
                const selectedSeries = document.querySelector('input[name="series"]:checked:not([value=""])');
                const allSelectedSeries = document.querySelectorAll('input[name="series"]:checked');

                console.log('Toutes les séries cochées:', allSelectedSeries);
                console.log('Série sélectionnée (non vide):', selectedSeries);

                if (!selectedSeries) {
                    this.showError('seriesError', 'Veuillez sélectionner une série pour la Première/Terminale');
                    isValid = false;
                } else {
                    // Effacer l'erreur si une série valide est sélectionnée
                    this.clearError(document.getElementById('seriesError'));
                }
            }
        }

        if (this.currentStep === 3) {
            // Check if at least one service is selected
            // const selectedServices = document.querySelectorAll('input[name="services"]:checked');
            // if (selectedServices.length === 0) {
            //     this.showError('servicesError', 'Veuillez sélectionner au moins un service');
            //     isValid = false;
            // }

            // Check if programme is selected
            const selectedProgramme = document.querySelector('input[name="programme"]:checked');
            if (!selectedProgramme) {
                this.showError('programmeError', 'Veuillez sélectionner un programme');
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
                case 'telephone':
                case 'telephone_parent':
                    const phoneRegex = /^[0-9\s\-\+\(\)]{8,}$/;
                    if (!phoneRegex.test(value)) {
                        errorMessage = 'Format de téléphone invalide';
                        isValid = false;
                    }
                    break;
                case 'date_naissance':
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
            `${document.getElementById('prenom').value} ${document.getElementById('nom').value}`;
        document.getElementById('summaryEmail').textContent =
            document.getElementById('email').value;
        document.getElementById('summaryPhone').textContent =
            document.getElementById('telephone').value;
        document.getElementById('summaryParent').textContent =
            document.getElementById('nom_parent').value;

        // Academic info summary
        const levelSelect = document.getElementById('niveau_etude');
        document.getElementById('summaryLevel').textContent =
            levelSelect.options[levelSelect.selectedIndex].text;
        document.getElementById('summarySchool').textContent =
            document.getElementById('etablissement_actuel').value;

        const mathSelect = document.getElementById('niveau_maths');
        let mathText = mathSelect.options[mathSelect.selectedIndex].text;
        mathText = mathText.replace(/\s*\(.*?\)\s*/g, '').trim();
        document.getElementById('summaryMathLevel').textContent = mathText;

        const scpSelect = document.getElementById('niveau_sp');
        let spText = scpSelect.options[scpSelect.selectedIndex].text;
        spText = spText.replace(/\s*\(.*?\)\s*/g, '').trim();
        document.getElementById('summarySPLevel').textContent = spText;

        const svtSelect = document.getElementById('niveau_svt');
        let svtText = svtSelect.options[svtSelect.selectedIndex].text;
        svtText = svtText.replace(/\s*\(.*?\)\s*/g, '').trim();
        document.getElementById('summarySVTLevel').textContent = svtText;

        // Course info summary
        const selectedProgram = document.querySelector('input[name="programme"]:checked');
        document.getElementById('summaryProgram').textContent =
            selectedProgram ? selectedProgram.nextElementSibling.querySelector('strong').textContent : '-';

        const selectedSubjects = Array.from(document.querySelectorAll('input[name="services"]:checked'))
            .map(cb => cb.value).join(', ');
        document.getElementById('summarySubjects').textContent = selectedSubjects || '-';

        // const startSelect = document.getElementById('startDate');
        // document.getElementById('summaryStartDate').textContent =
        //     startSelect.options[startSelect.selectedIndex].text;

        const scheduleSelect = document.getElementById('creneau');
        let creneauText = scheduleSelect.options[scheduleSelect.selectedIndex].text;
        creneauText = creneauText.replace(/\s*\(.*?\)\s*/g, '').trim();
        document.getElementById('summarySchedule').textContent = creneauText;

        // Price summary
        const selectedSubjectElements = document.querySelectorAll('input[name="subjects"]:checked');
        let monthlyTotal = 0;
        selectedSubjectElements.forEach(subject => {
            monthlyTotal += this.prices[subject.value] || 0;
        });

        document.getElementById('summaryMonthlyPrice').textContent = `${monthlyTotal}€`;
        document.getElementById('summaryTotalPrice').textContent = `${monthlyTotal + this.prices.inscription}€`;
    }

    // Fonction submitForm supprimée - la soumission se fait naturellement avec le bouton submit

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
