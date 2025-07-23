// Custom JavaScript para o ERP
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
            alertInstance.close();
        });
    }, 5000);
});

function showNotification(message, type = 'info', duration = 5000) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Implementação será expandida posteriormente
}
