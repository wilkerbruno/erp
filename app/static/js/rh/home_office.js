document.addEventListener('DOMContentLoaded', function() {
    carregarColaboradoresEmMultiplosSelects(['selectColabHO', 'selectColabAuxilio']);
    carregarAutorizacoes();
    carregarAuxiliosCelular();
    carregarContadoresHO();
});

function carregarContadoresHO() {
    fetch('/rh/api/home-office?status=todos')
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const lista = data.autorizacoes;
            document.getElementById('totalAtivas').textContent = lista.filter(a => a.status === 'ativo').length;
            document.getElementById('totalExpiradas').textContent = lista.filter(a => a.status === 'expirado').length;
            document.getElementById('totalCanceladas').textContent = lista.filter(a => a.status === 'cancelado').length;
        });
    fetch('/rh/api/auxilio-celular')
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') document.getElementById('totalAuxilios').textContent = data.total;
        });
}

function carregarAutorizacoes() {
    const status = document.getElementById('filtroStatusHO').value;
    const param = status !== 'todos' ? `?status=${status}` : '';
    fetch(`/rh/api/home-office${param}`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const tbody = document.getElementById('bodyAutorizacoes');
            if (data.autorizacoes.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhuma autorizacao encontrada</td></tr>';
                return;
            }
            const diasMap = { segunda:'Seg', terca:'Ter', quarta:'Qua', quinta:'Qui', sexta:'Sex' };
            tbody.innerHTML = data.autorizacoes.map(a => {
                const dias = a.dias_semana ? a.dias_semana.map(d => diasMap[d] || d).join(', ') : 'Todos';
                const periodo = a.data_inicio + (a.data_fim ? ` a ${a.data_fim}` : ' (indefinido)');
                const statusMap = { ativo:'success', expirado:'warning', cancelado:'secondary' };
                const badge = `<span class="badge bg-${statusMap[a.status] || 'secondary'}">${a.status}</span>`;
                const acoes = a.status === 'ativo'
                    ? `<button class="btn btn-sm btn-outline-danger" onclick="cancelarAutorizacao(${a.id})"><i class="fas fa-ban"></i></button>`
                    : '';
                return `<tr>
                    <td>${a.colaborador_nome || 'ID: ' + a.colaborador_id}</td>
                    <td>${periodo}</td>
                    <td>${dias}</td>
                    <td>${a.motivo || '-'}</td>
                    <td>${badge}</td>
                    <td>${acoes}</td>
                </tr>`;
            }).join('');
        });
}

function carregarAuxiliosCelular() {
    fetch('/rh/api/auxilio-celular')
        .then(r => r.json())
        .then(data => {
            if (data.status !== 'success') return;
            const tbody = document.getElementById('bodyAuxilios');
            if (data.auxilios.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum auxilio celular ativo</td></tr>';
                return;
            }
            tbody.innerHTML = data.auxilios.map(a => `<tr>
                <td>${a.colaborador_nome || 'ID: ' + a.colaborador_id}</td>
                <td>R$ ${a.valor_mensal.toFixed(2)}</td>
                <td>${a.data_inicio || '-'}</td>
                <td>${a.motivo_concessao || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="cancelarAuxilio(${a.id})">
                        <i class="fas fa-ban"></i> Cancelar
                    </button>
                </td>
            </tr>`).join('');
        });
}

function autorizarHomeOffice() {
    const form = document.getElementById('formAutorizarHomeOffice');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v, k) => { payload[k] = v; });

    const diasSemana = [];
    ['seg','ter','qua','qui','sex'].forEach(id => {
        const el = document.getElementById(id);
        if (el.checked) diasSemana.push(el.value);
    });
    if (diasSemana.length > 0) payload.dias_semana = diasSemana;
    if (payload.colaborador_id) payload.colaborador_id = parseInt(payload.colaborador_id);

    fetch('/rh/api/home-office', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalAutorizarHomeOffice')).hide();
            form.reset();
            carregarAutorizacoes();
            carregarContadoresHO();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => mostrarAlerta('danger', 'Erro ao autorizar home office'));
}

function cancelarAutorizacao(id) {
    if (!confirm('Deseja cancelar esta autorizacao?')) return;
    fetch(`/rh/api/home-office/${id}/cancelar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            carregarAutorizacoes();
            carregarContadoresHO();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    });
}

function concederAuxilioCelular() {
    const form = document.getElementById('formAuxilioCelular');
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((v, k) => { payload[k] = v; });
    if (payload.colaborador_id) payload.colaborador_id = parseInt(payload.colaborador_id);
    if (payload.valor_mensal) payload.valor_mensal = parseFloat(payload.valor_mensal);

    fetch('/rh/api/auxilio-celular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            bootstrap.Modal.getInstance(document.getElementById('modalAuxilioCelular')).hide();
            form.reset();
            carregarAuxiliosCelular();
            carregarContadoresHO();
            mostrarAlerta('success', data.message);
        } else {
            mostrarAlerta('danger', data.message);
        }
    })
    .catch(() => mostrarAlerta('danger', 'Erro ao conceder auxilio'));
}

function cancelarAuxilio(id) {
    if (!confirm('Cancelar este auxilio celular?')) return;
    fetch(`/rh/api/auxilio-celular/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                carregarAuxiliosCelular();
                carregarContadoresHO();
                mostrarAlerta('success', data.message);
            } else {
                mostrarAlerta('danger', data.message);
            }
        });
}