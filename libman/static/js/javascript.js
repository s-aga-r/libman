var Page_Base = {

    switchMode: function (isBtnClick = false) {
        // Get last saved mode from localStorage.
        var mode = window.localStorage.getItem("mode") == null ? "dark" : window.localStorage.getItem("mode");

        // Switch Button.
        var modeSwitcher = document.getElementById('mode');

        // Elements to change.
        var body = document.body;
        var navbar = document.getElementById('nav');
        var footer = document.getElementById('footer');
        var tables = document.getElementsByClassName('table');

        // Toggle between light and dark mode.
        function toggleMode() {
            // Body
            bodyClasses = ["bg-dark", "text-light", "bg-white", "text-dark"];
            bodyClasses.map(c => body.classList.toggle(c));
            // Navbar
            navbarClasses = ["navbar-dark", "bg-dark", "nav-border-bottom", "navbar-light", "bg-white", "border-bottom"];
            navbarClasses.map(c => navbar.classList.toggle(c));
            // Footer
            footerClasses = ["bg-dark", "footer-border", "bg-white", "border-top"];
            footerClasses.map(c => footer.classList.toggle(c));
            // Table
            tableClasses = ["table-dark"];
            tableClasses.map(c => {
                for (i = 0; i < tables.length; i++) {
                    tables[i].classList.toggle(c);
                }
            });
            // Switch mode icon
            iconClasses = ["mode-switch"];
            iconClasses.map(c => modeSwitcher.classList.toggle(c));
        }

        // Save mode value to localStorage.
        function saveToLocalStorage(value) {
            window.localStorage.setItem("mode", value);
        }

        // When user click on the switch icon.
        if (isBtnClick) {
            mode = mode == "dark" ? "light" : "dark";
            toggleMode();
        }
        // When page loads first time.
        else {
            if (mode == "light") {
                toggleMode();
            }
        }

        // Save current mode to localStorage.
        saveToLocalStorage(mode);
    }
}
