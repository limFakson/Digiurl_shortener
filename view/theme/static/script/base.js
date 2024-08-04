$.ajaxSetup({
    headers: {
        "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content"),
    },
});

$("#longurl").val("")

$(document).on('click', '.logo', function(e) {
    window.location.href = "/short/view/home"
})

function convert() {
    var longurl = $("#longurl").val();
    console.log(longurl);
    $.ajax({
        type: "POST",
        url: "/short/api/url",
        data: {
            url: longurl,
        },
        headers: {
            "Authorization": 'Token ' + localStorage.getItem('token')
        },

        success: function(data) {
            console.log(data["shorturl"]);
            $('#short').text("");
            $('.fa-copy').remove();
            var shorturl = data["shorturl"];
            var htmltext = '<p id="shorturl" class="inline-block pr-4 underline text-[#0d609b] cursor-copy">' + shorturl + "</p>";
            var icon = '<i class="fa-solid fa-copy"></i>'

            $('#short').append(htmltext);
            $('#copy').append(icon)
            $("#longurl").val("")
        },
        error: function(response) {
            console.log(response.responseJSON)
            if (response.responseJSON.message) {
                $('#error').text(response.responseJSON.message)
            }
        }
    });
}


$(document).on('click', "#copy", function(e) {
    var temp = $('<input/>')
    $("body").append(temp)
    temp.val($('#short').text()).select()
    document.execCommand("copy")
    temp.remove()
    console.log("copied")
    var alert = '<p class="underline text-base pt-2" id="alert">copied!!😎</p>'
    $('.short').append(alert)

    setTimeout(() => {
        const alert = document.getElementById('alert');
        if (alert) {
            alert.style.transition = "ease-in-out 3000s"
            alert.style.display = 'none';
        }
    }, 1000);
})

$(document).on('click', '#logout', function(e) {
    localStorage.removeItem('token')
})

function drop() {
    console.log('clicked');
    var drops = document.getElementById('drop');
    var icon = document.querySelector('#icon');

    if (drops.style.display === "none" || drops.style.display === "") {
        console.log("drop");
        drops.style.display = "block";
        drops.style.opacity = 1;
        drops.style.top = "2.3rem";
        drops.style.transform = "translatey(0px)";
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        drops.style.opacity = 0;
        drops.style.display = "none";
        drops.style.top = "0rem";
        drops.style.transform = "translatey(-15px)";
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
}

document.addEventListener('click', function(event) {
    var drops = document.getElementById('drop');
    var icon = document.querySelector('#icon');
    if (drops) {
        var isClickInside = drops.contains(event.target) || document.querySelector('#icon').contains(event.target);

        if (!isClickInside && drops.style.display === "block") {
            drops.style.opacity = 0;
            drops.style.display = "none";
            drops.style.top = "0rem";
            drops.style.transform = "translatey(-15px)";
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    }
});

const password = document.getElementById('password')
if (password) {
    password.addEventListener('focusout', function() {
        const password = this.value;
        const errorMessage = document.getElementById('error');
        const passwordField = document.querySelector('.password');
        const submitBtn = document.getElementsByClassName('submit-btn')

        if (password.length < 4) {
            errorMessage.textContent = "Password must be at least 4 characters.";
            passwordField.style.border = "1px solid red";
            submitBtn.disabled = true;
        } else {
            errorMessage.textContent = "";
            passwordField.style.border = "";
            submitBtn.disabled = false;
        }
    });
}

function hide() {
    document.getElementById('hide').checked = true;
    document.getElementById('reveal').checked = false;
    if (document.getElementById("hide").checked === true) {
        password.type = "text";
    }
}

function reveal() {
    document.getElementById('hide').checked = false;
    document.getElementById('reveal').checked = true;
    if (document.getElementById("hide").checked === false) {
        password.type = "password";
    }
}

$(document).on('click', '#login-submit-btn', function(e) {
    e.preventDefault()
    var credential = $('input[name="credential"]').val()
    var password = $('input[name="password"]').val()
    $.ajax({
        type: "POST",
        url: "/short/api/auth/login",
        data: {
            credential: credential,
            password: password
        },

        success: function(response) {
            localStorage.setItem('token', response.token)
            location.href = "/short/view/home"
        },
        error: function(response) {
            if (response.responseJSON.message) {
                $('#error').text(response.responseJSON.message).css('color', 'red')
            }
        }
    })
})

$(document).on('click', '#reg-submit-btn', function(e) {
    e.preventDefault()
    var username = $('input[name="username"]').val()
    var email = $('input[name="email"]').val()
    var password = $('input[name="password"]').val()
    $.ajax({
        type: "POST",
        url: "/short/api/auth/register",
        data: {
            username: username,
            email: email,
            password: password
        },

        success: function(response) {
            console.log(data)
            location.href = "/short/view/home"
        },
        error: function(response) {
            if (response.responseJSON.message) {
                $('#error').text(response.responseJSON.message)

            }
        }
    })
})