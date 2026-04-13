document.addEventListener('DOMContentLoaded', function() {
    criarGraficoEfoEvolucao();
    criarGraficoEfoDistribuicao();
});

function criarGraficoEfoEvolucao() {
    var ctx = document.getElementById('efoChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
            datasets: [{
                label: 'Score EFO Medio',
                data: [6.8, 7.0, 7.1, 7.2, 7.3, 7.2],
                borderColor: '#4e73df',
                backgroundColor: 'rgba(78, 115, 223, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: false, min: 6, max: 10 }
            }
        }
    });
}

function criarGraficoEfoDistribuicao() {
    var ctx = document.getElementById('distribuicaoChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Excelente (8-10)', 'Bom (6-8)', 'Regular (4-6)', 'Critico (0-4)'],
            datasets: [{
                data: [12, 25, 8, 0],
                backgroundColor: ['#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function novoDiagnostico() {
    window.location.href = '/efo/novo-diagnostico';
}

function verDiagnostico(id) {
    window.location.href = '/efo/diagnostico/' + id;
}