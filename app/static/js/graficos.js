function novaAcao() {
    alert('Funcionalidade em desenvolvimento');
}

function acessarFuncionalidade(nome) {
    alert('Funcionalidade "' + nome + '" será disponibilizada em breve!');
}

// Configuração dos gráficos
document.addEventListener('DOMContentLoaded', function() {
    
    // Gráfico Receitas vs Despesas
    const ctxReceitasDespesas = document.getElementById('receitasDespesasChart').getContext('2d');
    new Chart(ctxReceitasDespesas, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Receitas',
                data: [12000, 15000, 13000, 18000, 16000, 20000],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4
            }, {
                label: 'Despesas',
                data: [8000, 9000, 7500, 11000, 10000, 12000],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });

    // Gráfico Fluxo de Caixa
    const ctxFluxoCaixa = document.getElementById('fluxoCaixaChart').getContext('2d');
    new Chart(ctxFluxoCaixa, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Saldo',
                data: [4000, 6000, 5500, 7000, 6000, 8000],
                backgroundColor: [
                    '#28a745', '#28a745', '#28a745', 
                    '#28a745', '#28a745', '#28a745'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });

    // Gráfico Despesas por Categoria
    const ctxDespesasCategoria = document.getElementById('despesasCategoriaChart').getContext('2d');
    new Chart(ctxDespesasCategoria, {
        type: 'doughnut',
        data: {
            labels: ['Pessoal', 'Operacional', 'Marketing', 'Administrativo', 'Outros'],
            datasets: [{
                data: [35, 25, 15, 20, 5],
                backgroundColor: [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Gráfico Evolução Patrimonial
    const ctxEvolucaoPatrimonial = document.getElementById('evolucaoPatrimonialChart').getContext('2d');
    new Chart(ctxEvolucaoPatrimonial, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Patrimônio Líquido',
                data: [50000, 54000, 59500, 66500, 72500, 80500],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
});