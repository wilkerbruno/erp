document.addEventListener('DOMContentLoaded', function() {
    atualizarHorario();
    setInterval(atualizarHorario, 1000);
});

function acessarModulo(url) {
    window.location.href = url;
}

function atualizarHorario() {
    var agora = new Date();
    var opcoes = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    var elementoHorario = document.getElementById('current-time');
    if (elementoHorario) {
        elementoHorario.textContent = agora.toLocaleDateString('pt-BR', opcoes);
    }
}
