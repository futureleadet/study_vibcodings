document.addEventListener('DOMContentLoaded', () => {
    const appDiv = document.getElementById('app');
    const navLinks = document.querySelectorAll('.nav-link');

    // Function to load content into the #app div
    async function loadContent(page) {
        try {
            const response = await fetch(`${page}.html`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            appDiv.innerHTML = html;
        } catch (error) {
            console.error('Error loading page:', error);
            appDiv.innerHTML = '<p class="text-danger">페이지를 불러오는 데 실패했습니다.</p>';
        }
    }

    // Handle navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const page = event.target.getAttribute('href').substring(1); // Get page name from href (e.g., #home -> home)
            if (page) {
                loadContent(page);
            } else {
                // Default to home or login if href is just '#'
                loadContent('home'); // Assuming 'home.html' will be created later
            }

            // Update active class
            navLinks.forEach(nav => nav.classList.remove('active'));
            event.target.classList.add('active');
        });
    });

    // Load the login page initially
    loadContent('login');
});
