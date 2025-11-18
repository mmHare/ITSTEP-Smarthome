document.querySelectorAll('.navBar li a').forEach(
    link => {
        // if(link.href === window.location.href) {
        if(window.location.href.includes(link.href)) {
            link.setAttribute('aria-current', 'page')
        }
    }
)