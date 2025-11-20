document.querySelectorAll('.navBar li a').forEach(
    link => {
        // if(link.href === window.location.href) {
        if(window.location.href.includes("rooms")) {
            if(link.href.includes("rooms")) {
                link.setAttribute('aria-current', 'page')
            }
        }
        else if(!window.location.href.includes("rooms")) {
            if(window.location.href.includes(link.href)) {
                link.setAttribute('aria-current', 'page')
            }
        }
    }
)