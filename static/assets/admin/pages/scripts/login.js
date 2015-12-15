var Login = function() {

    var handleLogin = function() {

        $('.login-form').validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            rules: {
                username: {
                    required: true
                },
                password: {
                    required: true
                },
                remember: {
                    required: false
                }
            },

            messages: {
                username: {
                    required: "Username is required."
                },
                password: {
                    required: "Password is required."
                }
            },

            invalidHandler: function(event, validator) { //display error alert on form submit   
                $('.alert-danger', $('.login-form')).show();
            },

            highlight: function(element) { // hightlight error inputs
                $(element)
                    .closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function(label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function(error, element) {
                error.insertAfter(element.closest('.input-icon'));
            },

            submitHandler: function(form) {
                $.ajax({
                    url : "/login/",
                    type : "post",
                    data : $(form).serialize(),
                    success : function(response){
                        if(response.code===0){
                            window.location.href = response.text
                        } else {
                            bootbox.alert(response.text)
                        }
                    }
                })
            }
        });

        $('.login-form input').keypress(function(e) {
            if (e.which == 13) {
                if ($('.login-form').validate().form()) {
                    $('.login-form').submit(); //form validation success, call ajax form submit
                }
                return false;
            }
        });
    }

    var handleForgetPassword = function() {
        $('.forget-form').validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            ignore: "",
            rules: {
                email: {
                    required: true,
                    email: true
                }
            },

            messages: {
                email: {
                    required: "Email is required."
                }
            },

            invalidHandler: function(event, validator) { //display error alert on form submit   

            },

            highlight: function(element) { // hightlight error inputs
                $(element)
                    .closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function(label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function(error, element) {
                error.insertAfter(element.closest('.input-icon'));
            },

            submitHandler: function(form) {
                $.ajax({
                    url : "/sendmail/",
                    type : "post",
                    data : $(form).serialize(),
                    success : function(response){
                        bootbox.alert(response.text)
                    }
                })
            }
        });

        $('.forget-form input').keypress(function(e) {
            if (e.which == 13) {
                if ($('.forget-form').validate().form()) {
                    $('.forget-form').submit();
                }
                return false;
            }
        });

        jQuery('#forget-password').click(function() {
            jQuery('.login-form').hide();
            jQuery('.forget-form').show();
        });

        jQuery('#back-btn').click(function() {
            jQuery('.login-form').show();
            jQuery('.forget-form').hide();
        });

    }

    var handleRegister = function() {
        var $school,$grade,$klass
        function format(state) {
            if (!state.id) return state.text; // optgroup
            return "<img class='flag' src='../../assets/global/img/flags/" + state.id.toLowerCase() + ".png'/>&nbsp;&nbsp;" + state.text;
        }

        if (jQuery().select2) {
	        $("#select2_sample4").select2({
	            placeholder: '<i class="fa fa-map-marker"></i>&nbsp;Select a Country',
	            allowClear: true,
	            formatResult: format,
	            formatSelection: format,
	            escapeMarkup: function(m) {
	                return m;
	            }
	        });

	        $('#select2_sample4').change(function() {
	            $('.register-form').validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
	        });
    	}

        $school = $("#school")
        $grade = $("#grade")
        $klass = $("#klass")
        $school.change(function(event){
            var school_id=$school.val()
            $grade.find("option").remove()
            $klass.find("option").remove()
            if (!school_id){
               return
            }
            $.ajax({
                url : "/grade/" + school_id,
                type : "get",
                success : function(response){
                    $grade.append('<option value="" selected>请选择年级</option>')
                    for(index in response){
                        $grade.append("<option value="+response[index].id +">" + response[index].name + "</option>")
                    }
                }
            })
        })

        $grade.change(function(event){
            var grade_id = $grade.val()
            $klass.find("option").remove()
            if(!grade_id){
                return
            }

            $.ajax({
                url : '/klass/' + grade_id,
                type : 'get',
                success : function(response){
                    $klass.append('<option value="" selected>请选择班级</option>')
                    for (index in response){
                        $klass.append("<option value="+response[index].id +">" + response[index].name + "</option>")
                    }
                }
            })
        })

        $('.register-form').validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            ignore: "",
            rules: {

                first_name: {
                    required: true
                },
                sfzjh: {
                    required: true,
                    isidcardno:true,
                    remote:{
                        url:"/validator/User/sfzjh/",
                        type:"get"
                    }
                },
                email: {
                    required: true,
                    email: true,
                    remote : {
                        url : "/validator/User/email/",
                        type : "get"
                    }
                },
                school: {
                    required: true
                },
                grade: {
                    required: false
                },
                klass: {
                    required: false
                },
                username: {
                    remote:{
                        url:"/validator/User/username/",
                        type:"get"
                    }
                },
                password: {
                    required: true
                },
                rpassword: {
                    equalTo: "#register_password"
                },

                tnc: {
                    required: true
                }
            },

            messages: { // custom messages for radio buttons and checkboxes
                tnc: {
                    required: "Please accept TNC first."
                }
            },

            invalidHandler: function(event, validator) { //display error alert on form submit   

            },

            highlight: function(element) { // hightlight error inputs
                $(element)
                    .closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function(label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function(error, element) {
                if (element.attr("name") == "tnc") { // insert checkbox errors after the container                  
                    error.insertAfter($('#register_tnc_error'));
                } else if (element.closest('.input-icon').size() === 1) {
                    error.insertAfter(element.closest('.input-icon'));
                } else {
                    error.insertAfter(element);
                }
            },

            submitHandler: function(form) {
                bootbox.alert("hello")
                $.ajax({
                    url : "/register/",
                    type : "post",
                    data : $(form).serialize(),
                    success : function(response){
                        bootbox.alert(response.text)
                    }
                })
            }
        });

        $('.register-form input').keypress(function(e) {
            if (e.which == 13) {
                if ($('.register-form').validate().form()) {
                    $('.register-form').submit();
                }
                return false;
            }
        });

        jQuery('#register-btn').click(function() {
            jQuery('.login-form').hide();
            jQuery('.register-form').show();
        });

        jQuery('#register-back-btn').click(function() {
            jQuery('.login-form').show();
            jQuery('.register-form').hide();
        });
    }

    return {
        //main function to initiate the module
        init: function() {

            handleLogin();
            handleForgetPassword();
            handleRegister();

        }

    };

}();