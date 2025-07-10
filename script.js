document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', () => {
            document.getElementById('loading').style.display = 'block';
        });
    }
});



