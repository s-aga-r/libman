var Page_Base = {

    switchMode: function (isBtnClick = false) {
        // Elements to change.
        var body = document.body;
        var navbar = document.getElementById('nav');
        var footer = document.getElementById('footer');
        var tables = document.getElementsByClassName('table');

        // Switch Button.
        var modeSwitcher = document.getElementById('mode');

        // CSS Classes for Light and Dark mode.
        var darkBody = ["bg-dark", "text-light"];
        var lightBody = ["bg-white", "text-dark"];
        var darkNav = ["navbar-dark", "bg-dark", "nav-border-bottom"];
        var lightNav = ["navbar-light", "bg-white", "border-bottom"];
        var darkFooter = ["bg-dark", "footer-border"];
        var lightFooter = ["bg-white", "border-top"];
        var darkTable = ["table-dark"];
        var lightTable = [];

        // Get last saved mode from localStorage.
        var mode = window.localStorage.getItem("mode") == null ? "dark" : window.localStorage.getItem("mode");

        // Switch from Dark to Light mode.
        function switchToLight() {
            body.classList.remove(darkBody[0], darkBody[1]);
            body.classList.add(lightBody[0], lightBody[1]);
            navbar.classList.remove(darkNav[0], darkNav[1], darkNav[2]);
            navbar.classList.add(lightNav[0], lightNav[1], lightNav[2]);
            footer.classList.remove(darkFooter[0], darkFooter[1]);
            footer.classList.add(lightFooter[0], lightFooter[1]);

            for (i = 0; i < tables.length; i++) {
                var table = tables[i];
                table.classList.remove(darkTable[0]);
            }
        }

        // Switch from Light to Dark mode.
        function switchToDark() {
            body.classList.remove(lightBody[0], lightBody[1]);
            body.classList.add(darkBody[0], darkBody[1]);
            navbar.classList.remove(lightNav[0], lightNav[1], lightNav[2]);
            navbar.classList.add(darkNav[0], darkNav[1], darkNav[2]);
            footer.classList.remove(lightFooter[0], lightFooter[1]);
            footer.classList.add(darkFooter[0], darkFooter[1]);

            for (i = 0; i < tables.length; i++) {
                var table = tables[i];
                table.classList.add(darkTable[0]);
            }
        }

        // Save mode value to localStorage.
        function saveToLocalStorage(value) {
            window.localStorage.setItem("mode", value);
        }

        // Toggle the switch icon.
        function toggleIcon() {
            modeSwitcher.classList.toggle('mode-switch');
        }

        // When user click on the switch icon.
        if (isBtnClick) {
            if (mode == "dark") {
                switchToLight();
                mode = "light";
            }
            else {
                switchToDark();
                mode = "dark";
            }

            toggleIcon();
        }
        // When page loads first time.
        else {
            if (mode == "light") {
                switchToLight();
                toggleIcon();
            }
        }

        // Save current mode to localStorage.
        saveToLocalStorage(mode);
    }
}
