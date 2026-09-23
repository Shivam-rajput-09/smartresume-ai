// SmartResume AI — Client-Side Interactivity

document.addEventListener("DOMContentLoaded", function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // File input drag & drop feedback
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resume-input');
    const fileLabel = document.getElementById('file-chosen-label');

    if (dropZone && fileInput) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('border-primary', 'bg-light');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-primary', 'bg-light');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                fileInput.files = files;
                if (fileLabel) {
                    fileLabel.textContent = `Selected: ${files[0].name} (${(files[0].size / 1024).toFixed(1)} KB)`;
                }
            }
        });

        fileInput.addEventListener('change', function() {
            if (this.files.length > 0 && fileLabel) {
                fileLabel.textContent = `Selected: ${this.files[0].name} (${(this.files[0].size / 1024).toFixed(1)} KB)`;
            }
        });
    }
});
