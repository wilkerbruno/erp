let beneficiosCache = [];

document.addEventListener('DOMContentLoaded', function() {
    carregarBeneficios();
    carregarColaboradoresNoSelect('selectColaboradorVinculo');
    document.getElementById('selectColaboradorVinculo').addEventListener('change', function() {
        if (this.value) carregarBeneficiosColaborador(this.value);
        else document.getElementById('beneficiosColaborador').style.display = 'none';
    });
});

function carregarBeneficios() {
    const status = document.getElementById('filtroStatus').value;
    fetch(`/rh/api/beneficios?status=${status}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            beneficiosCache = data.beneficios;
            atualizarCardsBeneficios(data.beneficios);
            renderizarTabelaBeneficios(data.beneficios);
            atualizarSelectBeneficios(data.beneficios);
        });
}

function atualizarCardsBeneficios(beneficios) {
    const ativos = beneficios.filter(b => b.ativo);
    document.getElementById('totalBeneficios').textContent = ativos.length;
    document.getElementById('totalFixos').textContent = ativos.filter(b => b.tipo === 'fixo').length;
    document.getElementById('totalPercentuais').textContent = ativos.filter(b => b.tipo === 'percentual').length;
    document.getElementById('totalComRequisito').textContent = ativos.filter(b => b.requer_desempenho).length;
}

function renderizarTabelaBeneficios(beneficios) {
    const tbody = document.getElementById('bodyBeneficios');
    if (beneficios.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum beneficio encontrado</td></tr>';
        return;
    }
    tbody.innerHTML = beneficios.map(b => {
        let valor = '-';
        if (b.tipo === 'fixo' && b.valor_fixo) valor = `R$ ${parseFloat(b.valor_fixo).toFixed(2)}`;
        else if (b.tipo === 'percentual' && b.percentual) valor = `${parseFloat(b.percentual).toFixed(1)}%`;

        const statusBadge = b.ativo
            ? '<span class="badge bg-success">Ativo</span>'
            : '<span class="badge bg-secondary">Inativo</span>';

        const requisito = b.requer_desempenho
            ? `<span class="badge bg-warning text-dark">Meta ${b.meta_minima || 0}%</span>`
            : '<span class="text-muted">Nenhum</span>';

        return `<tr>
            <td><strong>${b.nome}</strong>${b.descricao ? '<br><small class="text-muted">' + b.descricao + '</small>' : ''}</td>
            <td><span class="badge bg-info">${b.tipo}</span></td>
            <td>${valor}</td>
            <td>${requisito}</td>
            <td>${statusBadge}</td>
            <td>
                <button class="btn btn-sm btn-outline-danger" onclick="desativarBeneficio(${b.id}, '${b.nome}')" ${!b.ativo ? 'disabled' : ''}>
                    <i class="fas fa-ban"></i>
                </button>
            </td>
        </tr>`;
    }).join('');
}

function atualizarSelectBeneficios(beneficios) {
    const select = document.getElementById('selectBeneficioVinculo');
    select.innerHTML = '<option value="">Selecione...</option>';
    beneficios.filter(b => b.ativo).forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.id;
        let texto = b.nome;
        if (b.tipo === 'fixo' && b.valor_fixo) texto += ` (R$ ${parseFloat(b.valor_fixo).toFixed(2)})`;
        opt.textContent = texto;
        select.appendChild(opt);
    });
}

function carregarBeneficiosColaborador(colaboradorId) {
    fetch(`/rh/api/colaboradores/${colaboradorId}/beneficios`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const container = document.getElementById('beneficiosColaborador');
            const tbody = document.getElementById('bodyBeneficiosColaborador');
            if (data.beneficios.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum beneficio vinculado</td></tr>';
            } else {
                tbody.innerHTML = data.beneficios.map(b => `<tr>
                    <td>${b.nome}</td>
                    <td>${b.tipo}</td>
                    <td>${b.valor ? 'R$ ' + b.valor.toFixed(2) : '-'}</td>
                    <td>${b.data_inicio || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger" onclick="desvincularBeneficio(${colaboradorId}, ${b.vinculo_id})">
                            <i class="fas fa-unlink"></i>
                        </button>
                    </td>
                </tr>`).join('');
            }
            container.style.display = 'block';
        });
}

function toggleCampoValor() {
    const tipo = document.getElementById('tipoBeneficio').value;
    document.getElementById('campoValorFixo').style.display = (tipo === 'fixo' || tipo === 'variavel') ? 'block' : 'none';
    document.getElementById('campoPercentual').style.display = tipo === 'percentual' ? 'block' : 'none';
}

function toggleMetaMinima() {
    document.getElementById('campoMetaMinima').style.display =
        document.getElementById('requerDesempenho').checked ? 'block' : 'none';
}

function criarBeneficio() {
    const form = document.getElementById('formNovoBeneficio');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v, k) => { payload[k] = v; });
    payload.requer_desempenho = document.getElementById('requerDesempenho').checked;
    if (payload.valor_fixo) payload.valor_fixo = parseFloat(payload.valor_fixo);
    if (payload.percentual) payload.percentual = parseFloat(payload.percentual);
    if (payload.meta_minima) payload.meta_minima = parseFloat(payload.meta_minima);

    fetch('/rh/api/beneficios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalNovoBeneficio')).hide();
            form.reset();
            carregarBeneficios();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => mostrarAlerta('danger', 'Erro ao criar beneficio'));
}

function desativarBeneficio(id, nome) {
    if (!confirm(`Desativar o beneficio "${nome}"?`)) return;
    fetch(`/rh/api/beneficios/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                carregarBeneficios();
                mostrarAlerta('success', data.message);
            } else {
                mostrarAlerta('danger', data.message);
            }
        });
}

function vincularBeneficio() {
    const colaboradorId = document.getElementById('selectColaboradorVinculo').value;
    const beneficioId = document.getElementById('selectBeneficioVinculo').value;
    if (!colaboradorId || !beneficioId) {
        mostrarAlerta('warning', 'Selecione colaborador e beneficio');
        return;
    }
    const payload = { beneficio_id: parseInt(beneficioId) };
    const valorCustom = document.getElementById('valorCustomizado').value;
    if (valorCustom) payload.valor_customizado = parseFloat(valorCustom);
    const dataInicio = document.getElementById('dataInicioVinculo').value;
    if (dataInicio) payload.data_inicio = dataInicio;

    fetch(`/rh/api/colaboradores/${colaboradorId}/beneficios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            carregarBeneficiosColaborador(colaboradorId);
            document.getElementById('valorCustomizado').value = '';
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    });
}

function desvincularBeneficio(colaboradorId, vinculoId) {
    if (!confirm('Desvincular este beneficio?')) return;
    fetch(`/rh/api/colaboradores/${colaboradorId}/beneficios/${vinculoId}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                carregarBeneficiosColaborador(colaboradorId);
                mostrarAlerta('success', data.message);
            } else {
                mostrarAlerta('danger', data.message);
            }
        });
}