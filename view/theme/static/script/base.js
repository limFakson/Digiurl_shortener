$.ajaxSetup({
  headers: {
    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
  }
})

var key = localStorage.getItem('token')

var authToken = key ? 'Token ' + key : ''

$(document).on('click', '.logo', function (e) {
  window.location.href = '/short/view/home'
})

function convert () {
  var spinner = '<div role="status">'
  spinner += '<svg aria-hidden="true" class="h-8 text-gray-200 animate-spin dark:text-gray-600 fill-[#f4f2f1] w-full text-center" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">'
  spinner += '<path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>'
  spinner += '<path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>'
  spinner += '</svg>'
  spinner += '<span class="sr-only">Loading...</span>'
  spinner += '</div>'

  $('#convert').text('')
  $('#convert').append(spinner)
  $('#convert').disabled

  var longurl = $('#longurl').val()
  console.log(longurl)
  $.ajax({
    type: 'POST',
    url: '/short/api/url',
    data: {
      url: longurl
    },
    headers: {
      'Authorization': authToken
    },

    success: function (data) {
      console.log(data['shorturl'])
      $('#error').text('')
      $('#short').text('')
      $('.fa-copy').remove()
      var shorturl = data['shorturl']
      var htmltext = '<p id="shorturl" class="inline-block pr-4 underline text-[#0d609b] cursor-copy">' + shorturl + '</p>'
      var icon = '<i class="fa-solid fa-copy"></i>'

      $('#short').append(htmltext)
      $('#copy').append(icon)
    },
    error: function (response) {
      console.log(response.responseJSON)
      $('#convert').text('')
      $('#convert').text('Shorten')
      if (response.responseJSON.message) {
        $('#error').text(response.responseJSON.message).css('color', 'red')
        setTimeout(() => {
          $('#error').text('')
        }, 1000)
      }
    }
  })
}

$(document).on('click', '#copy', function (e) {
  var temp = $('<input/>')
  $('body').append(temp)
  temp.val($('#short').text()).select()
  document.execCommand('copy')
  temp.remove()
  console.log('copied')
  $('.short').text('')
  var alert = '<p class="underline text-base pt-2" id="alert">copied!!😎</p>'
  $('.short').append(alert)
  $('#longurl').val('')

  setTimeout(() => {
    $('.short').text('')
    const alert = document.getElementById('alert')
    if (alert) {
      alert.style.transition = 'ease-in-out 3000s'
      alert.style.display = 'none'
    }
  }, 1000)
})

$(document).on('click', '#logout', function (e) {
  localStorage.removeItem('token')
})

function drop () {
  var drops = document.getElementById('drop')
  var icon = document.querySelector('#icon')

  if (drops.style.display === 'none' || drops.style.display === '') {
    console.log('drop')
    drops.style.display = 'block'
    drops.style.opacity = 1
    drops.style.top = '2.3rem'
    drops.style.transform = 'translatey(0px)'
    icon.classList.remove('fa-chevron-down')
    icon.classList.add('fa-chevron-up')
  } else {
    drops.style.opacity = 0
    drops.style.display = 'none'
    drops.style.top = '0rem'
    drops.style.transform = 'translatey(-15px)'
    icon.classList.remove('fa-chevron-up')
    icon.classList.add('fa-chevron-down')
  }
}

document.addEventListener('click', function (event) {
  var drops = document.getElementById('drop')
  var icon = document.querySelector('#icon')
  if (drops) {
    var isClickInside = drops.contains(event.target) || document.querySelector('#icon').contains(event.target)

    if (!isClickInside && drops.style.display === 'block') {
      drops.style.opacity = 0
      drops.style.display = 'none'
      drops.style.top = '0rem'
      drops.style.transform = 'translatey(-15px)'
      icon.classList.remove('fa-chevron-up')
      icon.classList.add('fa-chevron-down')
    }
  }
})

const password = document.getElementById('password')
if (password) {
  password.addEventListener('focusout', function () {
    const password = this.value
    const errorMessage = document.getElementById('error')
    const passwordField = document.querySelector('.password')
    const submitBtn = document.getElementsByClassName('submit-btn')
    submitBtn.disabled = true

    if (password.length < 6) {
      errorMessage.textContent = 'Password must be at least 6 characters.'
      passwordField.style.border = '1px solid red'
    } else {
      errorMessage.textContent = ''
      passwordField.style.border = ''
      submitBtn.disabled = false
    }
  })
}

function hide () {
  document.getElementById('hide').checked = true
  document.getElementById('reveal').checked = false
  if (document.getElementById('hide').checked === true) {
    password.type = 'text'
  }
}

function reveal () {
  document.getElementById('hide').checked = false
  document.getElementById('reveal').checked = true
  if (document.getElementById('hide').checked === false) {
    password.type = 'password'
  }
}

$(document).on('click', '#login-submit-btn', function (e) {
  var spinner = '<div role="status">'
  spinner += '<svg aria-hidden="true" class="h-8 text-gray-200 animate-spin dark:text-gray-600 fill-[#f4f2f1] w-full text-center" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">'
  spinner += '<path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>'
  spinner += '<path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>'
  spinner += '</svg>'
  spinner += '<span class="sr-only">Loading...</span>'
  spinner += '</div>'

  $(this).text('')
  $(this).append(spinner)
  $(this).disabled

  var credential = $('input[name="credential"]').val().toLowerCase()
  var password = $('input[name="password"]').val()
  $.ajax({
    type: 'POST',
    url: '/short/api/auth/login',
    data: {
      credential: credential,
      password: password
    },

    success: function (response) {
      localStorage.setItem('token', response.token)
      location.href = '/short/view/home'
    },
    error: function (response) {
      console.log(response.responseJSON)
      $('#login-submit-btn').text('')
      $('#login-submit-btn').text('Login')
      if (response.responseJSON.message) {
        $('#error').text(response.responseJSON.message).css('color', 'red')
      }else if (response.responseJSON.error) {
        $('#error').text(response.responseJSON.error).css('color', 'red')
      }
    }
  })
})

$(document).on('click', '.card-copy-btn', function (e) {
  var temp = $('<input/>')
  $('body').append(temp)
  temp.val($('#short').text()).select()
  document.execCommand('copy')
  temp.remove()
  console.log('copied')
  $('.card-alert').text('')
  var alert = '<p class="underline text-base pt-2" id="alert">copied!!😎</p>'
  $(this).closest('.link-card').find('.card-alert').append(alert)

  setTimeout(() => {
    $('.card-alert').text('')
    const alert = document.getElementById('card-alert')
    if (alert) {
      alert.style.transition = 'ease-in-out 3000s'
      alert.text('')
    }
  }, 1000)
})

$(document).on('click', '#reg-submit-btn', function (e) {
  var spinner = '<div role="status">'
  spinner += '<svg aria-hidden="true" class="h-8 text-gray-200 animate-spin dark:text-gray-600 fill-[#f4f2f1] w-full text-center" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">'
  spinner += '<path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>'
  spinner += '<path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>'
  spinner += '</svg>'
  spinner += '<span class="sr-only">Loading...</span>'
  spinner += '</div>'

  $(this).text('')
  $(this).append(spinner)
  $(this).disabled

  var username = $('input[name="username"]').val().toLowerCase()
  var email = $('input[name="email"]').val()
  var password = $('input[name="password"]').val()
  $.ajax({
    type: 'POST',
    url: '/short/api/auth/register',
    data: {
      username: username,
      email: email,
      password: password
    },

    success: function (response) {
      console.log(response.responseJSON)
      localStorage.setItem('token', response.token)
      location.href = '/short/view/home'
    },
    error: function (response) {
      console.log(response.responseJSON)
      $('#reg-submit-btn').text('')
      $('#reg-submit-btn').text('Register')
      if (response.responseJSON.message) {
        $('#error').text(response.responseJSON.message).css('color', 'red')
      } else if (response.responseJSON.password) {
        $('#error').text(response.responseJSON.password).css('color', 'red')
      }
    }
  })
})

function file () {
  $('input[name="profile_pics"]').click()
}

$(document).on('change', 'input[name="profile_pics"]', function (e) {
  const file = this.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = function (event) {
      console.log(event.target.result)
      $('.profile-photo').attr('src', event.target.result)
    }
    reader.readAsDataURL(file)
  }
})

$('#profile').on('click', '.edit-btn', function (event) {
  var bio = $('input[name="bio"]').val()
  var formData = new FormData()
  var profilePics = $('input[name="profile_pics"]')[0].files[0]

  console.log(profilePics)
  formData.append('bio', bio)
  formData.append('profile_pics', profilePics)

  $.ajax({
    type: 'POST',
    url: '/short/api/auth/profile',
    data: formData,
    contentType: false,
    processData: false,
    headers: {
      'Authorization': authToken
    },
    success: function (response) {
      console.log(response)
      location.href = '/short/view/profile'
    },
    error: function (response) {
      console.log(response)
      if (response.responseJSON.message) {
        $(this).disabled
        $('#error').text(response.responseJSON.message)
      } else if (response.responseJSON.error) {
        $(this).disabled
        $('#error').text(response.responseJSON.error)
      }
    }
  })
})

$(document).on('click', '.share-btn', function (e) {
  console.log('free')
  var link = $(this).parent().parent().parent().data('link')
  var encodedLink = encodeURIComponent(link)
  console.log(encodedLink)
  $('.share-tab').show().css('display', 'grid')
  $('input[name="copy-input[]"]').val(link)
  var currentHref = $('#social-link').attr('href')
  var newHref = currentHref + '' + encodedLink
  console.log(currentHref, newHref)

  $('#social-link').attr('href', newHref)
})

$(document).on('click', '.close', function (e) {
  $('.share-tab').hide()
})

$(document).on('click', '.copy-input button', function (e) {
  var temp = $('<input/>')
  $('body').append(temp)
  temp.val($('input[name="copy-input[]"]').val()).select()
  document.execCommand('copy')
  temp.remove()
  $(this).text('')
  $(this).append('copied')

  setTimeout(() => {
    $(this).text('')
    const alert = '<i class="fa-solid fa-copy pr-2"></i>Copy'
    if (alert) {
      $(this).css('transition', 'ease-in-out 3000s')
      $(this).append(alert)
    }
  }, 700)
})

// $(document).on('click', '.option-btn', function (e) {
//   var options = $(this).parent().find('.options')

//   if (options.css('display') === 'none' || options.css('display') === ' ') {
//     options.css('display', 'block')
//     setTimeout(() => {
//       options.css({ transform: 'translateX(0)', opacity: 1 }, 300)
//     }, 1)
//   // options.show()
//   } else {
//     options.css({ transform: 'translateX(50px)', opacity: 0 }, 300, function () {
//       // options.hide()
//     })
//     setTimeout(() => {
//       options.css('display', 'none')
//     }, 400)
//   }
// })

$(document).ready(function () {
  $(document).on('click', '.option-btn', function (e) {
    e.stopPropagation()
    var options = $(this).parent().find('.options')

    $('.options').not(options).css({transform: 'translateX(50px)', opacity: 0, display: 'none'})

    // Toggle the clicked options
    if (options.css('display') == 'none' || options.css('display') == '') {
      options.css('display', 'block')
      setTimeout(() => {
        options.css({ transform: 'translateX(0)', opacity: 1 })
      }, 0.2)
    } else {
      options.css({ transform: 'translateX(50px)', opacity: 0 })
      setTimeout(() => {
        options.css('display', 'none')
      }, 300)
    }
  })
})

// $(document).on('click', function () {
//   hideAllDropdowns()
// })

// const url = new URL(window.location.href)
// if (url) {
//   var newUrl = url.searchParams.get('edit')
//   if (newUrl == 'true') {
//     $('.edit-profile').css('display', 'grid')
//   }else {
//     $('.edit-profile').css('display', 'none')
//   }
// }

// $('.tab').on('click', '.close', function (e) {
//   const url = new URL(window.location.href)
//   url.searchParams.delete('edit')
//   history.replaceState(history.state, '', url.href)
//   $('.edit-profile').css('display', 'none')
// })

$('.profile-avater').on('click', '.edit-profile-btn span', function () {
  $('#error').text('')
  // $('.edit-profile').css('display', 'grid')
  $('.profile-avater .error').text('This feature is not available yet')
  setTimeout(() => {
    $('.profile-avater .error').text('')
  }, 1000)
})
$('.tab').on('click', '.close', function (e) {
  $('.edit-profile .tab').css('opacity', 1)
  setTimeout(() => {
    $('.edit-profile').css('display', 'none')
  }, 180)
})
