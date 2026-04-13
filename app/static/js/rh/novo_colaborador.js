document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('data_admissao').value = new Date().toISOString().split('T')[0];
    carregarCargos();
    carregarDepartamentosForm();

    document.getElementById('cpf').addEventListener('input', function(e) {
        var v = e.target.value.replace(/\D/g, '');
        if (v.length > 11) v = v.slice(0, 11);
        if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
        else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
        else if (v.length > 3) v = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
        e.target.value = v;
    });
});

function carregarCargos() {
    fetch('/rh/api/cargos')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                var select = document.getElementById('cargo_id');
                data.cargos.forEach(function(c) {
                    var opt = document.createElement('option');
                    opt.value = c.id;
                    opt.textContent = c.nome;
                    select.appendChild(opt);
                });
            }
        });
}

function carregarDepartamentosForm() {
    fetch('/rh/api/departamentos')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                var select = document.getElementById('departamento_id');
                data.departamentos.forEach(function(d) {
                    var opt = document.createElement('option');
                    opt.value = d.id;
                    opt.textContent = d.nome;
                    select.appendChild(opt);
                });
            }
        });
}

function salvarColaborador() {
    var form = document.getElementById('formColaborador');
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var btn = document.getElementById('btnSalvar');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Salvando...';

    var dados = {
        nome_completo: document.getElementById('nome_completo').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        rg: document.getElementById('rg').value.trim(),
        sexo: document.getElementById('sexo').value,
        data_nascimento: document.getElementById('data_nascimento').value || null,
        estado_civil: document.getElementById('estado_civil').value,
        email: document.getElementById('email').value.trim(),
        celular: document.getElementById('celular').value.trim(),
        cep: document.getElementById('cep').value.trim(),
        endereco: document.getElementById('endereco').value.trim(),
        numero: document.getElementById('numero').value.trim(),
        bairro: document.getElementById('bairro').value.trim(),
        cidade: document.getElementById('cidade').value.trim(),
        estado: document.getElementById('estado').value,
        cargo_id: document.getElementById('cargo_id').value || null,
        departamento_id: document.getElementById('departamento_id').value || null,
        data_admissao: document.getElementById('data_admissao').value,
        tipo_contrato: document.getElementById('tipo_contrato').value,
        salario_base: parseFloat(document.getElementById('salario_base').value) || null,
        jornada_trabalho: document.getElementById('jornada_trabalho').value.trim(),
        matricula: document.getElementById('matricula').value.trim() || null,
        banco: document.getElementById('banco').value.trim(),
        agencia: document.getElementById('agencia').value.trim(),
        conta: document.getElementById('conta').value.trim(),
        tipo_conta: document.getElementById('tipo_conta').value,
        pix: document.getElementById('pix').value.trim()
    };

    fetch('/rh/api/colaboradores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.status === 'success') {
            mostrarAlerta('success', 'Colaborador cadastrado com sucesso! Matricula: ' + data.colaborador.matricula);
            setTimeout(function() { window.location.href = '/rh/colaboradores'; }, 1500);
        } else {
            mostrarAlerta('danger', 'Erro: ' + data.message);
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar';
        }
    })
    .catch(function(err) {
        mostrarAlerta('danger', 'Erro de conexao: ' + err.message);
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-save me-1"></i>Salvar';
    });
}
