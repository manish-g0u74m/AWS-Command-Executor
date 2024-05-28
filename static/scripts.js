// static/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('awsForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);
        const prompts = formData.get('prompts').split('\n').filter(prompt => prompt.trim() !== ''); // Split prompts by line break

        // Fetch AWS commands output
        fetch('/execute', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            // Display output in output.html
            window.location.href = '/output';
        })
        .catch(error => console.error('Error:', error));
    });
});

