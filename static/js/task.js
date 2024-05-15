// Hide account navigation
const matchacc = document.querySelectorAll("a.nav-link.account")
matchacc.forEach((userItem) => {
    userItem.style.display = 'none'
});

const matchadm = document.querySelectorAll("a.nav-link.admin")
matchadm.forEach((userItem) => {
    userItem.style.display = 'none'
});

const matchalert = document.querySelectorAll("#alert")
matchalert.forEach((userItem) => {
    userItem.style.display = 'none'
});

document.querySelector("#alert_logout").style.display = 'none'
document.querySelector("#alert_delete_account").style.display = 'none'

// Show account navigation
function eventClick(){
    document.getElementById("acc").addEventListener('click', () => {
        if (matchacc[0].style.display == 'none'){
            matchacc.forEach((userItem) => {
                userItem.style.display = 'block'
            });
        }
        else{
            matchacc.forEach((userItem) => {
                userItem.style.display = 'none'
            });
        }
    })

    document.getElementById("adm").addEventListener('click', () => {
        if (matchadm[0].style.display == 'none'){
            matchadm.forEach((userItem) => {
                userItem.style.display = 'block'
            });
        }
        else{
            matchadm.forEach((userItem) => {
                userItem.style.display = 'none'
            });
        }
    })
}

// Show account alert
function alert(type) {   
    matchalert.forEach((userItem) => {
        userItem.style.display = 'block'
    });
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
        });
        document.querySelector("#alert_logout").style.display = 'none'
        document.querySelector("#alert_delete_account").style.display = 'none'
    }
}


eventClick()
