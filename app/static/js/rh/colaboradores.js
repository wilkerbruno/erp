document.addEventListener('DOMContentLoaded', function() {
    carregarEstatisticas();
    carregarDepartamentosSelect();
    carregarColaboradores();
    document.getElementById('filtBusca').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') carregarColaboradores();
    });
});

function carregarEstatisticas() {
    fetch('/rh/api/colaboradores/estatisticas')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                document.getElementById('cardTotal').textContent = data.total;
                document.getElementById('cardAtivos').textContent = data.ativos;
                document.getElementById('cardNovos').textContent = data.novos_mes;
                document.getElementById('cardDepartamentos').textContent = data.departamentos;
            }
        });
}

function carregarDepartamentosSelect() {
    fetch('/rh/api/departamentos')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                var select = document.getElementById('filtDepartamento');
                data.departamentos.forEach(function(dep) {
                    var opt = document.createElement('option');
                    opt.value = dep.id;
                    opt.textContent = dep.nome;
                    select.appendChild(opt);
                });
            }
        });
}

function carregarColaboradores() {
    var params = new URLSearchParams();
    var busca = document.getElementById('filtBusca').value;
    var dep = document.getElementById('filtDepartamento').value;
    var status = document.getElementById('filtStatus').value;
    if (busca) params.append('busca', busca);
    if (dep) params.append('departamento_id', dep);
    if (status) params.append('status', status);

    var corpo = document.getElementById('corpoTabela');
    corpo.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4"><i class="fas fa-spinner fa-spin me-2"></i>Carregando...</td></tr>';

    fetch('/rh/api/colaboradores?' + params.toString())
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                document.getElementById('badgeTotal').textContent = data.total + ' registros';
                renderizarTabelaColaboradores(data.colaboradores);
            } else {
                corpo.innerHTML = '<tr><td colspan="8" class="text-center text-danger py-4">Erro: ' + data.message + '</td></tr>';
            }
        })
        .catch(function(err) {
            corpo.innerHTML = '<tr><td colspan="8" class="text-center text-danger py-4">Erro de conexao: ' + err.message + '</td></tr>';
        });
}

function renderizarTabelaColaboradores(colaboradores) {
    var corpo = document.getElementById('corpoTabela');
    if (colaboradores.length === 0) {
        corpo.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">Nenhum colaborador encontrado</td></tr>';
        return;
    }
    var html = '';
    colaboradores.forEach(function(c) {
        var badge = c.ativo
            ? '<span class="badge bg-success">Ativo</span>'
            : '<span class="badge bg-danger">Inativo</span>';
        var dataAdm = c.data_admissao
            ? new Date(c.data_admissao + 'T00:00:00').toLocaleDateString('pt-BR')
            : '-';
        html += '<tr>' +
            '<td>' + (c.matricula || '-') + '</td>' +
            '<td><strong>' + c.nome_completo + '</strong></td>' +
            '<td>' + (c.cargo || '-') + '</td>' +
            '<td>' + (c.departamento || '-') + '</td>' +
            '<td>' + (c.email || '-') + '</td>' +
            '<td>' + dataAdm + '</td>' +
            '<td>' + badge + '</td>' +
            '<td>' +
                '<a href="/rh/colaborador/' + c.id + '" class="btn btn-sm btn-info me-1" title="Ver"><i class="fas fa-eye"></i></a>' +
                '<a href="/rh/colaborador/editar/' + c.id + '" class="btn btn-sm btn-warning me-1" title="Editar"><i class="fas fa-edit"></i></a>' +
                '<button class="btn btn-sm btn-danger" title="Desativar" onclick="desativarColaborador(' + c.id + ', \'' + c.nome_completo.replace(/'/g, "\\'") + '\')"><i class="fas fa-user-slash"></i></button>' +
            '</td></tr>';
    });
    corpo.innerHTML = html;
}

function desativarColaborador(id, nome) {
    if (!confirm('Desativar o colaborador ' + nome + '?')) return;
    var motivo = prompt('Motivo do desligamento:');
    if (motivo === null) return;

    fetch('/rh/api/colaboradores/' + id, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ motivo: motivo })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'success') {
            mostrarAlerta('success', data.message);
            carregarColaboradores();
            carregarEstatisticas();
        } else {
            mostrarAlerta('danger', 'Erro: ' + data.message);
        }
    });
}
