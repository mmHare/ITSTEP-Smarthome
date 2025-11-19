document.querySelectorAll('.tableStats th > button').forEach(
    button => {
        // if(window.location.href === 'http://127.0.0.1:8000/stats/sort/' + button.id + '/') {
        if(window.location.href.includes('http://127.0.0.1:8000/stats/sort/' + button.id)) {
            button.setAttribute('aria-current', 'page')
        }
    }
)