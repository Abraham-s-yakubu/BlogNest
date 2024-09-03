
document.addEventListener('DOMContentLoaded', function() {
    const alertBox = document.getElementById('success-alert');
    if (alertBox) {
        alertBox.style.display = 'block';
        setTimeout(function() {
            alertBox.style.display = 'none';
        }, 5000);  // Alert will disappear after 5 seconds
    }
});