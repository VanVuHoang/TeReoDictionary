// Hide account navigation
const matches = document.querySelectorAll("a#account.nav-link")
matches.forEach((userItem) => {
    userItem.style.display = 'none'
});

// Show account navigation
function eventClick(){
    document.getElementById("acc").addEventListener('click', () => {
        if (matches[0].style.display == 'none'){
            matches.forEach((userItem) => {
                userItem.style.display = 'block'
            });
        }
        else{
            matches.forEach((userItem) => {
                userItem.style.display = 'none'
            });
        }
    })
}

eventClick()