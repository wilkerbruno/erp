var API_BASE = '/rh/api';

document.addEventListener('DOMContentLoaded', function() {
    var hoje = new Date().toISOString().split('T')[0];
    document.getElementById('dataInicio').value = hoje;
    document.getElementById('dataFim').value = hoje;
    carregarColaboradoresPonto();
    carregarResumoDiario();
});

function carregarColaboradoresPonto() {
    fetch(API_BASE + '/colaboradores')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                var select = document.getElementById('colaboradorFiltro');
                data.colaboradores.forEach(function(c) {
                    var opt = document.createElement('option');
                    opt.value = c.id;
                    opt.textContent = c.nome;
                    select.appendChild(opt);
                });
            }
        })
        .catch(function(err) {
            // silencioso
        });
}

function carregarResumoDiario() {
    var dataInicio = document.getElementById('dataInicio').value;
    var dataFim = document.getElementById('dataFim').value;
    var colaboradorId = document.getElementById('colaboradorFiltro').value;
    var tbody = document.getElementById('corpoTabela');

    tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted py-5">' +
        '<i class="fas fa-spinner fa-spin fa-2x mb-3"></i><div>Carregando registros...</div></td></tr>';

    var url = API_BASE + '/resumo-diario?data_inicio=' + dataInicio + '&data_fim=' + dataFim;
    if (colaboradorId) url += '&colaborador_id=' + colaboradorId;

    fetch(url)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status !== 'success') throw new Error(data.message);
            var resumos = data.resumos;
            if (!resumos || resumos.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" class="text-center text-info py-5">' +
                    '<i class="fas fa-info-circle fa-2x mb-3"></i><div>Nenhum registro encontrado</div></td></tr>';
                document.getElementById('infoRegistros').textContent = 'Mostrando 0 registros';
                return;
            }
            tbody.innerHTML = '';
            resumos.forEach(function(r) {
                var atraso = calcularAtrasoTotal(r.registros);
                var badgeAtraso = atraso > 0
                    ? '<span class="badge bg-warning">' + atraso + ' min</span>'
                    : '<span class="badge bg-success">OK</span>';
                tbody.innerHTML += '<tr>' +
                    '<td>' + (r.colaborador_nome || 'ID ' + r.colaborador_id) + '</td>' +
                    '<td>' + formatarDataPonto(r.data) + '</td>' +
                    '<td>' + (r.entrada || '-') + '</td>' +
                    '<td>' + (r.saida_almoco || '-') + '</td>' +
                    '<td>' + (r.volta_almoco || '-') + '</td>' +
                    '<td>' + (r.saida || '-') + '</td>' +
                    '<td><strong>' + (r.total_horas || '0') + 'h</strong></td>' +
                    '<td>' + badgeAtraso + '</td>' +
                    '<td><button class="btn btn-sm btn-info" onclick=\'verDetalhes(' + JSON.stringify(r) + ')\'>' +
                    '<i class="fas fa-eye"></i></button></td></tr>';
            });
            document.getElementById('infoRegistros').textContent = 'Mostrando ' + resumos.length + ' registro(s)';
        })
        .catch(function(error) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center text-danger py-5">' +
                '<i class="fas fa-exclamation-triangle fa-2x mb-3"></i>' +
                '<div>Erro ao carregar registros</div>' +
                '<small class="text-muted d-block mt-2">' + error.message + '</small></td></tr>';
        });
}

function calcularAtrasoTotal(registros) {
    var total = 0;
    if (registros) {
        registros.forEach(function(r) {
            if (r.atraso_minutos) total += r.atraso_minutos;
        });
    }
    return total;
}

function formatarDataPonto(dataStr) {
    var d = new Date(dataStr + 'T00:00:00');
    return d.toLocaleDateString('pt-BR');
}

function filtrarRegistros() {
    carregarResumoDiario();
}

function atualizarLista() {
    carregarResumoDiario();
}

function verDetalhes(resumo) {
    var modal = new bootstrap.Modal(document.getElementById('modalDetalhes'));
    var conteudo = document.getElementById('conteudoDetalhes');
    var tipoNomes = {
        'entrada': 'Entrada',
        'saida_almoco': 'Saida Almoco',
        'volta_almoco': 'Volta Almoco',
        'saida': 'Saida'
    };
    var html = '<h6>Colaborador: ' + (resumo.colaborador_nome || 'ID ' + resumo.colaborador_id) + '</h6>' +
        '<p>Data: ' + formatarDataPonto(resumo.data) + '</p><hr>' +
        '<div class="table-responsive"><table class="table table-sm"><thead><tr>' +
        '<th>Tipo</th><th>Horario</th><th>Localizacao</th><th>Home Office</th></tr></thead><tbody>';
    if (resumo.registros) {
        resumo.registros.forEach(function(r) {
            html += '<tr><td>' + (tipoNomes[r.tipo] || r.tipo) + '</td>' +
                '<td>' + r.horario + '</td>' +
                '<td>' + (r.localizacao_texto || '-') + '</td>' +
                '<td>' + (r.home_office ? '<i class="fas fa-check text-success"></i>' : '-') + '</td></tr>';
        });
    }
    html += '</tbody></table></div>' +
        '<div class="alert alert-info mt-3"><strong>Total de Horas Trabalhadas:</strong> ' +
        (resumo.total_horas || '0') + 'h</div>';
    conteudo.innerHTML = html;
    modal.show();
}

function exportarExcel() {
    mostrarAlerta('info', 'Funcionalidade de exportacao sera implementada em breve');
}
