// Query selection
const matchacc = document.querySelectorAll("a.nav-link.account")
matchacc.forEach((userItem) => {
    userItem.style.display = 'none'
})

const matchadm = document.querySelectorAll("a.nav-link.admin")
matchadm.forEach((userItem) => {
    userItem.style.display = 'none'
})

const matchalert = document.querySelectorAll("#alert")
matchalert.forEach((userItem) => {
    userItem.style.display = 'none'
})

const matchcheckbox = document.querySelectorAll("input[type=checkbox]")


// Disable edit
function disabled(match){
    match.forEach((userItem) => {
        // Checking either "Password" or "Confirm Password" affects both
        if (userItem.disabled == true){
            userItem.disabled = false
            if (userItem.classList.contains('password')){
                document.querySelector("input[type=checkbox].password#password").checked = true
                document.querySelector("input[type=checkbox].password#password2").checked = true
            }
        }
        else{
            userItem.disabled = true
            if (userItem.classList.contains('password')){
                document.querySelector("input[type=checkbox].password#password").checked = false
                document.querySelector("input[type=checkbox].password#password2").checked = false
            }
        }
    })
}

matchcheckbox.forEach((userItem) => {
    userItem.addEventListener('click', () => {
        disabled(document.querySelectorAll(`select.${userItem.className}`))
        disabled(document.querySelectorAll(`input[type=text].${userItem.className}`))
        disabled(document.querySelectorAll(`input[type=email].${userItem.className}`))
        disabled(document.querySelectorAll(`input[type=password].${userItem.className}`))
        disabled(document.querySelectorAll(`input[type=radio].${userItem.className}`))
    })
})


// Show account navigation
function eventClick(){
    document.getElementById("acc").addEventListener('click', () => {
        if (matchacc[0].style.display == 'none'){
            matchacc.forEach((userItem) => {
                userItem.style.display = 'block'
            })
        }
        else{
            matchacc.forEach((userItem) => {
                userItem.style.display = 'none'
            })
        }
    })

    document.getElementById("adm").addEventListener('click', () => {
        if (matchadm[0].style.display == 'none'){
            matchadm.forEach((userItem) => {
                userItem.style.display = 'block'
            })
        }
        else{
            matchadm.forEach((userItem) => {
                userItem.style.display = 'none'
            })
        }
    })
}


// Show account alert
function alert(type) {  
    if (Number.isInteger(type)){
        // Loop until the right item
        let i = 0
        let j = 0
        const matchdelcfm = document.querySelectorAll("#delete_word_confirm")
        matchdelcfm.forEach((userItem) => {
            i = i + 1
            if (i == type){
                userItem.style.display = 'none'
            }
        })
        const matchdel = document.querySelectorAll("#delete_word")
        console.log(matchdel)
        matchdel.forEach((userItem) => {
            j = j + 1
            if (j == type){
                userItem.style.display = 'block'
            }
        })
    }
    else{
        matchalert.forEach((userItem) => {
            userItem.style.display = 'block'
        })
        // Corresponding alert
        if (type == 'logout'){
            document.querySelector("#alert_logout").style.display = 'block'
            document.querySelector("#alert_delete_account").style.display = 'none'
        }
        if (type == 'delete_account'){
            document.querySelector("#alert_logout").style.display = 'none'
            document.querySelector("#alert_delete_account").style.display = 'block'
        }
        if (type == ''){
            matchalert.forEach((userItem) => {
                userItem.style.display = 'none'
            })
            document.querySelector("#alert_logout").style.display = 'none'
            document.querySelector("#alert_delete_account").style.display = 'none'
        }
    }
}


eventClick()