
function novoProjeto() {
    new bootstrap.Modal(document.getElementById('modalNovoProjeto')).show();
}

function editarProjeto(id) {
    alert(`Editando projeto ${id}`);
}

function verDetalhes(id) {
    alert(`Detalhes do projeto ${id}`);
}

function cronograma(id) {
    window.location.href = '/consultoria/cronogramas?projeto=' + id;
}

function relatorio(id) {
    alert(`Relatório do projeto ${id}`);
}

function salvarProjeto() {
    alert('Projeto salvo com sucesso!');
    bootstrap.Modal.getInstance(document.getElementById('modalNovoProjeto')).hide();
}

function filtrarProjetos() {
    // Lógica de filtro aqui
    console.log('Filtrando projetos...');
}

function limparFiltros() {
    document.getElementById('filtroStatus').value = '';
    document.getElementById('filtroCliente').value = '';
    document.getElementById('filtroConsultor').value = '';
    filtrarProjetos();
}

function exportarProjetos() {
    alert('Exportando projetos para Excel...');
}

console.log('Página de Projetos carregada!');
