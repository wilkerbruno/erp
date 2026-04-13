document.addEventListener('DOMContentLoaded', function() {
    criarGraficoReceitasDespesas();
    criarGraficoFluxoCaixa();
    criarGraficoDespesasCategoria();
    criarGraficoEvolucaoPatrimonial();
});

function criarGraficoReceitasDespesas() {
    var ctx = document.getElementById('receitasDespesasChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
            datasets: [{
                label: 'Receitas',
                data: [450000, 520000, 480000, 580000, 620000, 590000, 650000, 680000],
                backgroundColor: 'rgba(40, 167, 69, 0.8)'
            }, {
                label: 'Despesas',
                data: [320000, 380000, 350000, 420000, 450000, 430000, 480000, 510000],
                backgroundColor: 'rgba(220, 53, 69, 0.8)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + (value / 1000).toFixed(0) + 'k';
                        }
                    }
                }
            }
        }
    });
}

function criarGraficoFluxoCaixa() {
    var ctx = document.getElementById('fluxoCaixaChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
            datasets: [{
                label: 'Saldo',
                data: [100000, 130000, 160000, 140000, 170000, 190000, 210000, 170000],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: { responsive: true }
    });
}

function criarGraficoDespesasCategoria() {
    var ctx = document.getElementById('despesasCategoriaChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Fornecedores', 'Salarios', 'Impostos', 'Despesas', 'Outros'],
            datasets: [{
                data: [40, 30, 15, 10, 5],
                backgroundColor: ['#dc3545', '#28a745', '#ffc107', '#17a2b8', '#6c757d']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function criarGraficoEvolucaoPatrimonial() {
    var ctx = document.getElementById('evolucaoPatrimonialChart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
            datasets: [{
                label: 'Patrimonio Liquido',
                data: [800000, 820000, 850000, 870000, 890000, 920000, 940000, 960000],
                borderColor: 'rgba(40, 167, 69, 1)',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: { responsive: true }
    });
}

function atualizarDados() {
    location.reload();
}