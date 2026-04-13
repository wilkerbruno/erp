var localizacaoAtual = null;
var colaboradorId = 1;

document.addEventListener('DOMContentLoaded', function() {
    atualizarRelogio();
    setInterval(atualizarRelogio, 1000);
    obterLocalizacao();
    carregarRegistrosHoje();
    setInterval(carregarRegistrosHoje, 30000);
});

function atualizarRelogio() {
    var agora = new Date();
    var horas = String(agora.getHours()).padStart(2, '0');
    var minutos = String(agora.getMinutes()).padStart(2, '0');
    var segundos = String(agora.getSeconds()).padStart(2, '0');
    document.getElementById('relogio').textContent = horas + ':' + minutos + ':' + segundos;
    var opcoes = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('data').textContent = agora.toLocaleDateString('pt-BR', opcoes);
}

function obterLocalizacao() {
    if (!navigator.geolocation) {
        document.getElementById('statusLocalizacao').innerHTML =
            '<span class="badge bg-danger">Navegador nao suporta geolocalizacao</span>';
        return;
    }
    navigator.geolocation.getCurrentPosition(
        function(position) {
            localizacaoAtual = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
            document.getElementById('statusLocalizacao').innerHTML =
                '<span class="badge bg-success">Localizacao Obtida</span>';
            obterEndereco(localizacaoAtual.latitude, localizacaoAtual.longitude);
            var distancia = calcularDistancia(
                localizacaoAtual.latitude, localizacaoAtual.longitude,
                -7.13, -34.83
            );
            document.getElementById('distanciaEmpresa').textContent =
                'Distancia da empresa: ' + distancia.toFixed(0) + 'm';
        },
        function() {
            document.getElementById('statusLocalizacao').innerHTML =
                '<span class="badge bg-danger">Erro ao obter localizacao</span>';
        }
    );
}

function obterEndereco(lat, lon) {
    fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lon)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var endereco = data.display_name || 'Endereco nao disponivel';
            document.getElementById('enderecoTexto').textContent = endereco;
        })
        .catch(function() {
            document.getElementById('enderecoTexto').textContent = 'Nao foi possivel obter endereco';
        });
}

function calcularDistancia(lat1, lon1, lat2, lon2) {
    var R = 6371e3;
    var p1 = lat1 * Math.PI / 180;
    var p2 = lat2 * Math.PI / 180;
    var dp = (lat2 - lat1) * Math.PI / 180;
    var dl = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dp / 2) * Math.sin(dp / 2) +
            Math.cos(p1) * Math.cos(p2) *
            Math.sin(dl / 2) * Math.sin(dl / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function carregarRegistrosHoje() {
    var url = '/rh/api/ponto/hoje/' + colaboradorId;
    fetch(url)
        .then(function(response) {
            if (response.status === 404 || response.status === 302 || response.status === 401) {
                return { status: 'success', registros: [] };
            }
            var contentType = response.headers.get('Content-Type');
            if (!contentType || contentType.indexOf('application/json') === -1) {
                return { status: 'success', registros: [] };
            }
            return response.json();
        })
        .then(function(data) {
            var div = document.getElementById('registrosHoje');
            if (!data || data.status !== 'success' || !data.registros || data.registros.length === 0) {
                div.innerHTML = '<div class="col-12 text-center text-muted py-3">' +
                    '<i class="fas fa-info-circle me-2"></i>Nenhum registro hoje</div>';
                return;
            }
            var tipoIcons = {
                'entrada': 'sign-in-alt text-success',
                'saida_almoco': 'utensils text-warning',
                'volta_almoco': 'coffee text-info',
                'saida': 'sign-out-alt text-danger'
            };
            var tipoNomes = {
                'entrada': 'Entrada',
                'saida_almoco': 'Saida Almoco',
                'volta_almoco': 'Volta Almoco',
                'saida': 'Saida'
            };
            div.innerHTML = '';
            data.registros.forEach(function(r) {
                var icon = tipoIcons[r.tipo] || 'clock text-secondary';
                var nome = tipoNomes[r.tipo] || r.tipo;
                var atraso = r.atraso_minutos || 0;
                div.innerHTML += '<div class="col-md-6 col-lg-3 mb-3">' +
                    '<div class="card ' + (atraso > 0 ? 'border-warning' : '') + '">' +
                    '<div class="card-body text-center p-3">' +
                    '<i class="fas fa-' + icon + ' fa-2x mb-2"></i>' +
                    '<div><strong>' + nome + '</strong></div>' +
                    '<div class="text-primary fs-4"><strong>' + r.horario + '</strong></div>' +
                    (r.home_office ? '<span class="badge bg-info mt-1">Home Office</span>' : '') +
                    (atraso > 0 ? '<span class="badge bg-warning text-dark mt-1">' + atraso + ' min atraso</span>' : '') +
                    '</div></div></div>';
            });
        })
        .catch(function() {
            var div = document.getElementById('registrosHoje');
            div.innerHTML = '<div class="col-12 text-center text-muted py-3">' +
                '<i class="fas fa-info-circle me-2"></i>Nenhum registro hoje</div>';
        });
}

function registrarPonto(tipo) {
    if (!localizacaoAtual) {
        mostrarAlerta('warning', 'Aguarde a obtencao da localizacao');
        return;
    }
    var agora = new Date();
    var homeOffice = document.getElementById('checkHomeOffice') ?
                     document.getElementById('checkHomeOffice').checked : false;
    var dados = {
        colaborador_id: colaboradorId,
        data: agora.toISOString().split('T')[0],
        horario: agora.toTimeString().split(' ')[0],
        tipo: tipo,
        latitude: localizacaoAtual.latitude,
        longitude: localizacaoAtual.longitude,
        localizacao_texto: document.getElementById('enderecoTexto') ?
                           document.getElementById('enderecoTexto').textContent : 'Nao disponivel',
        home_office: homeOffice,
        dispositivo: navigator.userAgent
    };

    fetch('/rh/api/registrar-ponto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(function(response) {
        var contentType = response.headers.get('Content-Type');
        if (!contentType || contentType.indexOf('application/json') === -1) {
            throw new Error('Servidor retornou resposta invalida. Status: ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        if (data.status === 'success') {
            var msg = 'Ponto registrado - ' + tipo + ' as ' + dados.horario;
            if (data.atraso_minutos > 0) msg += ' (atraso: ' + data.atraso_minutos + ' min)';
            if (homeOffice) {
                msg += data.home_office_autorizado
                    ? ' - Home Office autorizado'
                    : ' - Home Office NAO autorizado pelo gestor';
            }
            mostrarAlerta('success', msg);
            carregarRegistrosHoje();
        } else {
            mostrarAlerta('danger', 'Erro: ' + (data.message || 'Erro desconhecido'));
        }
    })
    .catch(function(error) {
        mostrarAlerta('danger', 'Erro ao registrar ponto: ' + error.message);
    });
}
