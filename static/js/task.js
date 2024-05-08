// Hide account navigation
const matchacc = document.querySelectorAll("a#account.nav-link")
matchacc.forEach((userItem) => {
    userItem.style.display = 'none'
});

const matchadm = document.querySelectorAll("a#admin.nav-link")
matchadm.forEach((userItem) => {
    userItem.style.display = 'none'
});

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

eventClick()
