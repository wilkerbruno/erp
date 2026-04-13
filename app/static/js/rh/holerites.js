let holeritesList = [];

document.addEventListener('DOMContentLoaded', function() {
    carregarColaboradoresEmMultiplosSelects(['selectColabHolerite', 'filtroColaborador']);
    filtrarHolerites();
});

function filtrarHolerites() {
    const params = new URLSearchParams();
    const mes = document.getElementById('filtroMes').value;
    const ano = document.getElementById('filtroAno').value;
    const colab = document.getElementById('filtroColaborador').value;
    const status = document.getElementById('filtroStatusHolerite').value;
    if (mes) params.set('mes', mes);
    if (ano) params.set('ano', ano);
    if (colab) params.set('colaborador_id', colab);
    if (status) params.set('status', status);

    fetch(`/rh/api/holerites?${params.toString()}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            holeritesList = data.holerites;
            atualizarCardsHolerites(data.holerites);
            renderizarTabelaHolerites(data.holerites);
        });
}

function atualizarCardsHolerites(holerites) {
    document.getElementById('totalHolerites').textContent = holerites.length;
    document.getElementById('totalPagos').textContent = holerites.filter(h => h.status === 'pago').length;
    document.getElementById('totalGerados').textContent = holerites.filter(h => h.status === 'gerado').length;
    document.getElementById('totalEnviados').textContent = holerites.filter(h => h.status === 'enviado').length;
}

function renderizarTabelaHolerites(holerites) {
    const tbody = document.getElementById('bodyHolerites');
    if (holerites.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Nenhum holerite encontrado</td></tr>';
        return;
    }
    const meses = ['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
    tbody.innerHTML = holerites.map(h => {
        const statusMap = { gerado:'warning', enviado:'info', pago:'success' };
        const badge = `<span class="badge bg-${statusMap[h.status] || 'secondary'}">${h.status}</span>`;
        return `<tr>
            <td>${h.colaborador_nome || 'ID: ' + h.colaborador_id}</td>
            <td>${meses[h.mes]}/${h.ano}</td>
            <td>R$ ${parseFloat(h.salario_base).toFixed(2)}</td>
            <td class="text-success">R$ ${parseFloat(h.total_vencimentos).toFixed(2)}</td>
            <td class="text-danger">R$ ${parseFloat(h.total_descontos).toFixed(2)}</td>
            <td><strong>R$ ${parseFloat(h.liquido).toFixed(2)}</strong></td>
            <td>${badge}</td>
            <td>
                <button class="btn btn-sm btn-outline-info" onclick="visualizarHolerite(${h.id})" title="Detalhes">
                    <i class="fas fa-eye"></i>
                </button>
                ${h.status !== 'pago' ? `
                <button class="btn btn-sm btn-outline-success" onclick="marcarComoPago(${h.id})" title="Marcar como Pago">
                    <i class="fas fa-check"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="excluirHolerite(${h.id})" title="Excluir">
                    <i class="fas fa-trash"></i>
                </button>` : ''}
            </td>
        </tr>`;
    }).join('');
}

function gerarHolerite() {
    const form = document.getElementById('formGerarHolerite');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v, k) => {
        payload[k] = ['colaborador_id','mes','ano','faltas_quantidade','atrasos_quantidade'].includes(k)
            ? parseInt(v) : parseFloat(v) || v;
    });

    fetch('/rh/api/holerites/gerar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalGerarHolerite')).hide();
            form.reset();
            filtrarHolerites();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => mostrarAlerta('danger', 'Erro ao gerar holerite'));
}

function gerarHoleritesLote() {
    const mes = parseInt(document.getElementById('selectMesLote').value);
    const ano = parseInt(document.getElementById('inputAnoLote').value);
    if (!confirm(`Gerar holerites para TODOS os colaboradores ativos em ${mes}/${ano}?`)) return;

    const btn = document.getElementById('btnGerarLote');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Gerando...';

    fetch('/rh/api/holerites/gerar-lote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mes: mes, ano: ano })
    })
    .then(r => r.json())
    .then(data => {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-layer-group me-1"></i>Gerar para Todos';
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalGerarLote')).hide();
            filtrarHolerites();
            let msg = data.message;
            if (data.erros && data.erros.length > 0) {
                msg += '\n\nAvisos:\n' + data.erros.join('\n');
            }
            mostrarAlerta('success', msg);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-layer-group me-1"></i>Gerar para Todos';
        mostrarAlerta('danger', 'Erro ao gerar holerites em lote');
    });
}

function visualizarHolerite(id) {
    fetch(`/rh/api/holerites/${id}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const h = data.holerite;
            const d = h.detalhes;
            const meses = ['','Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
            document.getElementById('bodyDetalhesHolerite').innerHTML = `
                <h5 class="text-center mb-3">${h.colaborador_nome} - ${meses[h.mes]}/${h.ano}</h5>
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-success">Vencimentos</h6>
                        <table class="table table-sm">
                            <tr><td>Salario Base</td><td class="text-end">R$ ${parseFloat(h.salario_base).toFixed(2)}</td></tr>
                            ${d.horas_extras > 0 ? `<tr><td>Horas Extras</td><td class="text-end">R$ ${d.horas_extras.toFixed(2)}</td></tr>` : ''}
                            ${d.adicional_noturno > 0 ? `<tr><td>Adic. Noturno</td><td class="text-end">R$ ${d.adicional_noturno.toFixed(2)}</td></tr>` : ''}
                            ${d.comissoes > 0 ? `<tr><td>Comissoes</td><td class="text-end">R$ ${d.comissoes.toFixed(2)}</td></tr>` : ''}
                            ${d.bonus > 0 ? `<tr><td>Bonus</td><td class="text-end">R$ ${d.bonus.toFixed(2)}</td></tr>` : ''}
                            ${d.vale_alimentacao > 0 ? `<tr><td>Vale Alimentacao</td><td class="text-end">R$ ${d.vale_alimentacao.toFixed(2)}</td></tr>` : ''}
                            ${d.vale_transporte > 0 ? `<tr><td>Vale Transporte</td><td class="text-end">R$ ${d.vale_transporte.toFixed(2)}</td></tr>` : ''}
                            ${d.auxilio_celular > 0 ? `<tr><td>Auxilio Celular</td><td class="text-end">R$ ${d.auxilio_celular.toFixed(2)}</td></tr>` : ''}
                            ${d.plano_saude > 0 ? `<tr><td>Plano Saude</td><td class="text-end">R$ ${d.plano_saude.toFixed(2)}</td></tr>` : ''}
                            ${d.outros_beneficios > 0 ? `<tr><td>Outros Beneficios</td><td class="text-end">R$ ${d.outros_beneficios.toFixed(2)}</td></tr>` : ''}
                            <tr class="fw-bold"><td>Total Vencimentos</td><td class="text-end text-success">R$ ${parseFloat(h.total_vencimentos).toFixed(2)}</td></tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-danger">Descontos</h6>
                        <table class="table table-sm">
                            <tr><td>INSS</td><td class="text-end">R$ ${d.inss.toFixed(2)}</td></tr>
                            <tr><td>IRRF</td><td class="text-end">R$ ${d.irrf.toFixed(2)}</td></tr>
                            ${d.vale_transporte_desconto > 0 ? `<tr><td>VT (desconto)</td><td class="text-end">R$ ${d.vale_transporte_desconto.toFixed(2)}</td></tr>` : ''}
                            ${d.plano_saude_desconto > 0 ? `<tr><td>Plano Saude (desc.)</td><td class="text-end">R$ ${d.plano_saude_desconto.toFixed(2)}</td></tr>` : ''}
                            ${d.faltas > 0 ? `<tr><td>Faltas</td><td class="text-end">R$ ${d.faltas.toFixed(2)}</td></tr>` : ''}
                            ${d.atrasos > 0 ? `<tr><td>Atrasos</td><td class="text-end">R$ ${d.atrasos.toFixed(2)}</td></tr>` : ''}
                            ${d.adiantamento > 0 ? `<tr><td>Adiantamento</td><td class="text-end">R$ ${d.adiantamento.toFixed(2)}</td></tr>` : ''}
                            ${d.emprestimos > 0 ? `<tr><td>Emprestimos</td><td class="text-end">R$ ${d.emprestimos.toFixed(2)}</td></tr>` : ''}
                            <tr class="fw-bold"><td>Total Descontos</td><td class="text-end text-danger">R$ ${parseFloat(h.total_descontos).toFixed(2)}</td></tr>
                        </table>
                        <hr>
                        <h6>Bases de Calculo</h6>
                        <table class="table table-sm">
                            <tr><td>Base INSS</td><td class="text-end">R$ ${d.base_inss.toFixed(2)}</td></tr>
                            <tr><td>Base IRRF</td><td class="text-end">R$ ${d.base_irrf.toFixed(2)}</td></tr>
                            <tr><td>Base FGTS</td><td class="text-end">R$ ${d.base_fgts.toFixed(2)}</td></tr>
                            <tr><td>FGTS (8%)</td><td class="text-end">R$ ${d.fgts.toFixed(2)}</td></tr>
                        </table>
                    </div>
                </div>
                <div class="text-center mt-3 p-3 bg-light rounded">
                    <h4>Liquido: <span class="text-primary">R$ ${parseFloat(h.liquido).toFixed(2)}</span></h4>
                </div>`;
            new bootstrap.Modal(document.getElementById('modalDetalhesHolerite')).show();
        });
}

function marcarComoPago(id) {
    if (!confirm('Marcar este holerite como pago?')) return;
    fetch(`/rh/api/holerites/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'pago', data_pagamento: new Date().toISOString().split('T')[0] })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            filtrarHolerites();
            mostrarAlerta('success', 'Holerite marcado como pago');
        } else {
            mostrarAlerta('danger', data.message);
        }
    });
}

function excluirHolerite(id) {
    if (!confirm('Excluir este holerite? Esta acao nao pode ser desfeita.')) return;
    fetch(`/rh/api/holerites/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                filtrarHolerites();
                mostrarAlerta('success', data.message);
            } else {
                mostrarAlerta('danger', data.message);
            }
        });
}