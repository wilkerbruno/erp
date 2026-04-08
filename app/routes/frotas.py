from flask import render_template
from flask_login import login_required
from app import app


@app.route('/frotas/')
@login_required
def frotas_index():
    return render_template('frotas/index.html')


@app.route('/frotas/combustivel')
@login_required
def frotas_combustivel():
    return render_template('frotas/combustivel/index.html')


@app.route('/frotas/combustivel/registrar')
@login_required
def frotas_registrar_combustivel():
    return render_template('frotas/combustivel/registrar.html')


@app.route('/frotas/documentacao')
@login_required
def frotas_documentacao():
    return render_template('frotas/documentacao/index.html')


@app.route('/frotas/documentacao/alertas')
@login_required
def frotas_alertas_documentacao():
    return render_template('frotas/documentacao/alertas.html')


@app.route('/frotas/manutencao')
@login_required
def frotas_manutencao():
    return render_template('frotas/manutencao/index.html')


@app.route('/frotas/manutencao/agendar')
@login_required
def frotas_agendar_manutencao():
    return render_template('frotas/manutencao/agendar.html')


@app.route('/frotas/motoristas')
@login_required
def frotas_motoristas():
    return render_template('frotas/motoristas/index.html')


@app.route('/frotas/motoristas/novo')
@login_required
def frotas_novo_motorista():
    return render_template('frotas/motoristas/novo.html')


@app.route('/frotas/rastreamento')
@login_required
def frotas_rastreamento():
    return render_template('frotas/rastreamento/mapa.html')


@app.route('/frotas/historico')
@login_required
def frotas_historico_rastreamento():
    return render_template('frotas/rastreamento/historico.html')


@app.route('/frotas/mapa')
@login_required
def frotas_mapa_rastreamento():
    return render_template('frotas/rastreamento/mapa.html')


@app.route('/frotas/relatorios')
@login_required
def frotas_relatorios():
    return render_template('frotas/relatorios/index.html')


@app.route('/frotas/relatorios/custos')
@login_required
def frotas_relatorios_custos():
    return render_template('frotas/relatorios/custos.html')


@app.route('/frotas/relatorios/geral')
@login_required
def frotas_relatorios_geral():
    return render_template('frotas/relatorios/geral.html')


@app.route('/frotas/relatorios/manutencao')
@login_required
def frotas_relatorios_manutencao():
    return render_template('frotas/relatorios/manutencao.html')


@app.route('/frotas/relatorios/viagens')
@login_required
def frotas_relatorios_viagens():
    return render_template('frotas/relatorios/viagens.html')


@app.route('/frotas/seguros')
@login_required
def frotas_seguros():
    return render_template('frotas/seguros/index.html')


@app.route('/frotas/veiculos')
@login_required
def frotas_veiculos():
    return render_template('frotas/veiculos/index.html')


@app.route('/frotas/veiculos/detalhes/<int:veiculo_id>')
@login_required
def frotas_detalhes_veiculo(veiculo_id):
    return render_template('frotas/veiculos/detalhes.html', veiculo_id=veiculo_id)


@app.route('/frotas/veiculos/novo')
@login_required
def frotas_novo_veiculo():
    return render_template('frotas/veiculos/novo.html')


@app.route('/frotas/viagens')
@login_required
def frotas_viagens():
    return render_template('viagens/index.html')


@app.route('/frotas/viagens/nova')
@login_required
def frotas_viagens_nova():
    return render_template('viagens/nova.html')


@app.route('/frotas/viagens/editar/<int:viagem_id>')
@login_required
def frotas_viagens_editar(viagem_id):
    return render_template('viagens/editar.html', viagem_id=viagem_id)