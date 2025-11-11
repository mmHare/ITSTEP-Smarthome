let darkmode = localStorage.getItem('darkmode')
const themeSwitch = document.getElementById('theme-switch')

const enableDarkmode = () => {
    document.body.classList.add('darkmode')     // dodaje klasę do 'body' htmla
    localStorage.setItem('darkmode', 'active')  // można przechowywać tylko stringi, dlatego 'active', a nie 'True'/'False'
}

const disableDarkmode = () => {
    document.body.classList.remove('darkmode')
    localStorage.setItem('darkmode', null)
}

if(darkmode === "active") enableDarkmode()      // przy ładowaniu strony sprawdza czy lokalnie był włączony darkmode

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode') // sprawdza stan darkmode przy każdym kliknięciu
    
    darkmode !== "active" ? enableDarkmode() : disableDarkmode() // list comprehension?:p
    // ^ szybszy syntax niż: 
    // if(darkmode !== "active"){
    //     enableDarkmode()
    // }
    // else{
    //     disableDarkmode()
    // }
})