       /* switch for desplaying hamburger menu , summary and filter and etc for mobile*/
       function switchClass(eid, cname) {
        /*get html elements*/
            const nav = document.getElementById(eid);
            /* compare the current layout.*/
            if (nav.classList.contains(cname)) {
                /*if current layout is cname (has cname), remove the cname layout(remove cname).*/
                nav.classList.remove(cname)
            } else {
                /*if current is not cname, add cname layout (add cname)*/
                nav.classList.add(cname)
            }
        }
        /*call switchclass function for hamburger menu*/
        function switchNav() {
            switchClass('floatNav', 'nav-active')
        }