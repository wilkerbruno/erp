function formatarMoeda(valor) {
    return 'R$ ' + parseFloat(valor).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function carregarColaboradoresNoSelect(seletorId, filtroStatus) {
    var status = filtroStatus || 'ativos';
    return fetch('/rh/api/colaboradores?status=' + status)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status !== 'success') return [];
            var select = document.getElementById(seletorId);
            if (!select) return data.colaboradores;
            var primeiraOpcao = select.querySelector('option');
            select.innerHTML = '';
            if (primeiraOpcao) select.appendChild(primeiraOpcao);
            data.colaboradores.forEach(function(c) {
                var opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.nome_completo;
                select.appendChild(opt);
            });
            return data.colaboradores;
        });
}

function carregarColaboradoresEmMultiplosSelects(ids) {
    return fetch('/rh/api/colaboradores?status=ativos')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status !== 'success') return;
            ids.forEach(function(id) {
                var select = document.getElementById(id);
                if (!select) return;
                var primeiraOpcao = select.querySelector('option');
                select.innerHTML = '';
                if (primeiraOpcao) select.appendChild(primeiraOpcao);
                data.colaboradores.forEach(function(c) {
                    var opt = document.createElement('option');
                    opt.value = c.id;
                    opt.textContent = c.nome_completo;
                    select.appendChild(opt);
                });
            });
        });
}