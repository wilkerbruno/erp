document.addEventListener('DOMContentLoaded', function() {
    criarGraficoMargens();
    criarGraficoComposicao();
});

function criarGraficoMargens() {
    var ctx = document.getElementById('graficoMargens');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
            datasets: [{
                label: 'Margem Bruta',
                data: [38, 39, 40, 41, 40, 39, 40, 40],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4
            }, {
                label: 'Margem EBITDA',
                data: [12, 13, 14, 15, 14, 13, 14, 14],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4
            }, {
                label: 'Margem Liquida',
                data: [5, 5.5, 6, 6.5, 6, 5.5, 6, 6],
                borderColor: '#ffc107',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, max: 50 } }
        }
    });
}

function criarGraficoComposicao() {
    var ctx = document.getElementById('graficoComposicao');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: ['Custo Produtos', 'Desp. Operacionais', 'Desp. Financeiras', 'Impostos', 'Lucro Liquido'],
            datasets: [{
                data: [60, 26, 3, 5, 6],
                backgroundColor: ['#dc3545', '#ffc107', '#17a2b8', '#6c757d', '#28a745']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function atualizarDRE() {
    mostrarAlerta('info', 'Atualizando DRE...');
}

function compararPeriodos() {
    mostrarAlerta('info', 'Funcionalidade de comparacao em desenvolvimento');
}

function exportarDRE() {
    mostrarAlerta('info', 'Exportando DRE para Excel...');
}