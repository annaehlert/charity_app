document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */


        //     var es = document.getElementsByTagName('a')
        //     for(var i=0; i<es.length; i++){
        //       es[i].addEventListener('click', function(e) {
        //     e.preventDefault()
        //     document.location.hash = e.target.getAttribute('href')
        //   })
        // }

        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            // this.$element = form.querySelector("div.form-group.form-group--checkbox input[name='categories']");
            // this.$institution = form.querySelector("div.form-group.form-group--checkbox input[name='organization']");

            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // // TODO: Validation
            const element = document.querySelectorAll("div.form-group.form-group--checkbox input[name='categories']");
            const institutions = document.querySelectorAll("div.form-group.form-group--checkbox input[name='institution']");
            // const element = document.getElementsByName('categories');
            // const institutions = document.getElementsByName('organization');
            // const description = institution.nextElementSibling;
            //
            //
            for (var i = 0; i < Object.keys(category_list).length; i++) {
                var key = Object.keys(category_list)[i];
                for (var j = 0; j < institutions.length; j++) {
                    var institution_value = institutions[j].value;
                    if (key === element[i].value && element[i].checked === true) {
                        // var zmienna = Object.values(category_list)[i].includes(institution_value);
                        // console.log(Object.values(category_list)[i]);
                        // console.log(institution_value);


                        if (Object.values(category_list)[i].includes(Number(institution_value))) {
                            console.log("udało się");
                            institutions[j].parentElement.parentElement.style.display = "block";
                        } else {
                            institutions[j].parentElement.parentElement.style.display = "none";
                            console.log("Ide");
                        }
                    }

                }
            }
            //
            // if (element[j].checked === true) {
            //     institutions[i].parentElement.parentElement.style.display = "block";
            // } else {
            //     institutions[i].parentElement.parentElement.style.display = "none";
            // }
            //
            // for (var i = 0; i < institutions.length; i++) {
            //     for (var j = 0; j < element.length; j++) {
            //         var key = Object.keys(category_list)[j];
            //         var category_value = category_list[key];
            //         var institution_value = institutions[i].value;
            //
            // $.each(category_list, function (key, value){
            //     if(jQuery.inArray(institution_value, value) !== -1){
            //         console.log(institution_value);
            //     }else{
            //         console.log('dupa');
            //     }
            // });
            // $.each(category_value, function () {
            //     if (jQuery.inArray(institution_value, category_value) !== -1) {
            //         // if(value.includes(institution_value)){
            //         console.log(institution_value);
            //     }
            // });
            //
            //
            //         if (element[j].checked === true) {
            //             institutions[i].parentElement.parentElement.style.display = "block";
            //         } else {
            //             institutions[i].parentElement.parentElement.style.display = "none";
            //         }
            //     }
            // }


            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         *

         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
            $.ajax({
                url: "http://127.0.0.1:8000/add-donation/",
                type: "POST",
                dataType: 'json',
                data: {
                // $('form#donation').serialize()

                categories: $('#categories').val(),
                quantity: $('#quantity').val(),
                institution: $('#institution').val(),
                address: $('#address').val(),
                city: $('#city').val(),
                zip_code: $('#zip_code').val(),
                phone_number: $('#phone_number').val(),
                pick_up_date: $('#pick_up_date').val(),
                pick_up_time: $('#pick_up_time').val(),
                pick_up_comment: $('#pick_up_comment').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
            }).done(function (response) {
                if (response.success === "ok"){
                    window.location = "http://127.0.0.1:8000/add-donation/confirmation/"
                }else if(response.success === "form_error"){
                    console.log(response.errors);
                }
                else{
                    alert('Coś poszło nie tak, spróbuj jeszcze raz.');
                }

            })
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
