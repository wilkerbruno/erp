let graficoEvolucao = null;

document.addEventListener('DOMContentLoaded', function() {
    carregarRegistrosDRE();
    carregarEvolucao();
});

function carregarRegistrosDRE() {
    const ano = document.getElementById('filtroAnoDRE').value;
    const param = ano ? `?ano=${ano}` : '';
    fetch(`/rh/api/dre${param}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            atualizarCardsDRE(data.registros);
            renderizarTabelaDRE(data.registros);
        });
}

function atualizarCardsDRE(registros) {
    if (registros.length === 0) {
        ['cardReceitaBruta','cardLucroBruto','cardResultadoLiquido','cardMargemLiquida'].forEach(id => {
            document.getElementById(id).textContent = '-';
        });
        return;
    }
    const ultimo = registros[0];
    document.getElementById('cardReceitaBruta').textContent = formatarMoeda(ultimo.receita_bruta);
    document.getElementById('cardLucroBruto').textContent = formatarMoeda(ultimo.lucro_bruto);
    document.getElementById('cardResultadoLiquido').textContent = formatarMoeda(ultimo.resultado_liquido);
    document.getElementById('cardMargemLiquida').textContent = ultimo.margem_liquida ? ultimo.margem_liquida.toFixed(1) + '%' : '-';
}

function renderizarTabelaDRE(registros) {
    const tbody = document.getElementById('bodyDRE');
    const meses = ['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
    if (registros.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Nenhum registro DRE encontrado</td></tr>';
        return;
    }
    tbody.innerHTML = registros.map(r => {
        const resLiqClass = parseFloat(r.resultado_liquido) >= 0 ? 'text-success' : 'text-danger';
        return `<tr>
            <td>${meses[r.mes]}/${r.ano}</td>
            <td>${formatarMoeda(r.receita_bruta)}</td>
            <td>${formatarMoeda(r.receita_liquida)}</td>
            <td>${formatarMoeda(r.lucro_bruto)}</td>
            <td>${formatarMoeda(r.resultado_operacional)}</td>
            <td class="${resLiqClass} fw-bold">${formatarMoeda(r.resultado_liquido)}</td>
            <td>${r.margem_liquida ? r.margem_liquida.toFixed(1) + '%' : '-'}</td>
            <td>
                <button class="btn btn-sm btn-outline-info" onclick="verDetalhesDRE(${r.id})" title="Detalhes"><i class="fas fa-eye"></i></button>
                <button class="btn btn-sm btn-outline-danger" onclick="excluirDRE(${r.id})" title="Excluir"><i class="fas fa-trash"></i></button>
            </td>
        </tr>`;
    }).join('');
}

function carregarEvolucao() {
    const ano = document.getElementById('filtroAnoEvolucao').value;
    const param = ano ? `?ano=${ano}` : '?meses=12';
    fetch(`/rh/api/dre/evolucao${param}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            renderizarGrafico(data.evolucao);
        });
}

function renderizarGrafico(evolucao) {
    const ctx = document.getElementById('graficoEvolucao').getContext('2d');
    if (graficoEvolucao) graficoEvolucao.destroy();

    if (evolucao.length === 0) {
        graficoEvolucao = new Chart(ctx, {
            type: 'line',
            data: { labels: ['Sem dados'], datasets: [{ label: 'Sem dados', data: [0] }] }
        });
        return;
    }

    graficoEvolucao = new Chart(ctx, {
        type: 'line',
        data: {
            labels: evolucao.map(e => e.periodo),
            datasets: [
                {
                    label: 'Receita Liquida',
                    data: evolucao.map(e => e.receita_liquida),
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Lucro Bruto',
                    data: evolucao.map(e => e.lucro_bruto),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Resultado Liquido',
                    data: evolucao.map(e => e.resultado_liquido),
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatarMoeda(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
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

function salvarDRE() {
    const form = document.getElementById('formNovaDRE');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v, k) => {
        payload[k] = ['mes','ano'].includes(k) ? parseInt(v) : parseFloat(v) || v;
    });

    fetch('/rh/api/dre', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalImportarDRE')).hide();
            form.reset();
            carregarRegistrosDRE();
            carregarEvolucao();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => mostrarAlerta('danger', 'Erro ao salvar DRE'));
}

function verDetalhesDRE(id) {
    fetch(`/rh/api/dre/${id}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const d = data.dre.detalhes;
            const meses = ['','Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
            document.getElementById('bodyDetalhesDRE').innerHTML = `
                <h5 class="text-center mb-4">DRE - ${meses[data.dre.mes]}/${data.dre.ano}</h5>
                <table class="table table-sm">
                    <tr class="table-light"><td colspan="2"><strong>RECEITAS</strong></td></tr>
                    <tr><td>Receita Bruta</td><td class="text-end">${formatarMoeda(d.receita_bruta)}</td></tr>
                    <tr><td>(-) Deducoes</td><td class="text-end text-danger">${formatarMoeda(d.deducoes)}</td></tr>
                    <tr class="fw-bold"><td>= Receita Liquida</td><td class="text-end">${formatarMoeda(d.receita_liquida)}</td></tr>
                    <tr class="table-light"><td colspan="2"><strong>CUSTOS</strong></td></tr>
                    <tr><td>(-) CMV</td><td class="text-end text-danger">${formatarMoeda(d.custo_mercadorias)}</td></tr>
                    <tr><td>(-) Custo Servicos</td><td class="text-end text-danger">${formatarMoeda(d.custo_servicos)}</td></tr>
                    <tr class="fw-bold text-success"><td>= Lucro Bruto</td><td class="text-end">${formatarMoeda(d.lucro_bruto)}</td></tr>
                    <tr class="table-light"><td colspan="2"><strong>DESPESAS OPERACIONAIS</strong></td></tr>
                    <tr><td>(-) Desp. Vendas</td><td class="text-end text-danger">${formatarMoeda(d.despesas_vendas)}</td></tr>
                    <tr><td>(-) Comissoes Vendas</td><td class="text-end text-danger">${formatarMoeda(d.comissoes_vendas)}</td></tr>
                    <tr><td>(-) Desp. Administrativas</td><td class="text-end text-danger">${formatarMoeda(d.despesas_administrativas)}</td></tr>
                    <tr><td>(-) Salarios e Encargos</td><td class="text-end text-danger">${formatarMoeda(d.salarios_encargos)}</td></tr>
                    <tr><td>(-) Aluguel</td><td class="text-end text-danger">${formatarMoeda(d.aluguel)}</td></tr>
                    <tr class="table-light"><td colspan="2"><strong>RESULTADO FINANCEIRO</strong></td></tr>
                    <tr><td>(-) Desp. Financeiras</td><td class="text-end text-danger">${formatarMoeda(d.despesas_financeiras)}</td></tr>
                    <tr><td>(+) Rec. Financeiras</td><td class="text-end text-success">${formatarMoeda(d.receitas_financeiras)}</td></tr>
                    <tr class="fw-bold"><td>= Resultado Operacional</td><td class="text-end">${formatarMoeda(d.resultado_operacional)}</td></tr>
                    <tr><td>(-) Impostos/Contrib.</td><td class="text-end text-danger">${formatarMoeda(d.impostos_contribuicoes)}</td></tr>
                    <tr class="fw-bold fs-5 ${parseFloat(d.resultado_liquido) >= 0 ? 'text-success' : 'text-danger'}">
                        <td>= RESULTADO LIQUIDO</td><td class="text-end">${formatarMoeda(d.resultado_liquido)}</td>
                    </tr>
                </table>
                <div class="row mt-3">
                    <div class="col-md-4 text-center"><small class="text-muted">Margem Bruta</small><br><strong>${d.margem_bruta ? d.margem_bruta + '%' : '-'}</strong></div>
                    <div class="col-md-4 text-center"><small class="text-muted">Margem Operacional</small><br><strong>${d.margem_operacional ? d.margem_operacional + '%' : '-'}</strong></div>
                    <div class="col-md-4 text-center"><small class="text-muted">Margem Liquida</small><br><strong>${d.margem_liquida ? d.margem_liquida + '%' : '-'}</strong></div>
                </div>`;
            new bootstrap.Modal(document.getElementById('modalDetalhesDRE')).show();
        });
}

function excluirDRE(id) {
    if (!confirm('Excluir este registro DRE?')) return;
    fetch(`/rh/api/dre/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                carregarRegistrosDRE();
                carregarEvolucao();
                mostrarAlerta('success', data.message);
            } else {
                mostrarAlerta('danger', data.message);
            }
        });
}