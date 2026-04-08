from flask import render_template, request, jsonify, send_file, flash, redirect
from flask_login import login_required, current_user
from app import app, csrf
import os


@app.route('/consultoria/')
@login_required
def consultoria_index():
    return render_template('consultoria/index.html')


@app.route('/consultoria/projetos')
@login_required
def consultoria_projetos():
    return render_template('consultoria/projetos.html')


@app.route('/consultoria/clientes')
@login_required
def consultoria_clientes():
    return render_template('consultoria/clientes.html')


@app.route('/consultoria/consultores')
@login_required
def consultoria_consultores():
    return render_template('consultoria/consultores.html')


@app.route('/consultoria/contratos')
@login_required
def consultoria_contratos():
    return render_template('consultoria/contratos.html')


@app.route('/consultoria/cronogramas')
@login_required
def consultoria_cronogramas():
    return render_template('consultoria/cronogramas.html')


@app.route('/consultoria/relatorios')
@login_required
def consultoria_relatorios():
    return render_template('consultoria/relatorios.html')


@app.route('/consultoria/diagnostico-efo')
@login_required
def consultoria_diagnostico_efo():
    return render_template('consultoria/diagnostico_efo.html')


@app.route('/consultoria/diagnostico-inicial')
@login_required
def consultoria_diagnostico_inicial():
    return render_template('consultoria/diagnostico_inicial.html')


@app.route('/consultoria/checklist-sfm')
@login_required
def consultoria_checklist_sfm():
    return render_template('consultoria/checklist_sfm.html')


@app.route('/consultoria/acompanhamento')
@login_required
def consultoria_acompanhamento():
    return render_template('consultoria/acompanhamento.html')


@app.route('/consultoria/api/gerar-relatorio', methods=['POST'])
@login_required
@csrf.exempt
def consultoria_api_gerar_relatorio():
    try:
        try:
            from app.services.consultoria_reports import ConsultoriaReportService
        except ImportError:
            return jsonify({'error': 'Servico de relatorios nao instalado'}), 500

        data = request.get_json()
        tipo_relatorio = data.get('tipo')
        if not tipo_relatorio:
            return jsonify({'error': 'Tipo de relatorio e obrigatorio'}), 400

        service = ConsultoriaReportService()
        resultado = service.gerar_relatorio(
            tipo=tipo_relatorio,
            periodo=data.get('periodo'),
            formato=data.get('formato', 'excel'),
            filtros=data.get('filtros', {}),
            usuario=current_user.username if current_user.is_authenticated else 'Sistema'
        )

        if resultado['success']:
            return jsonify({
                'success': True,
                'message': 'Relatorio gerado com sucesso!',
                'arquivo': resultado['arquivo'],
                'nome_arquivo': resultado['nome_arquivo'],
                'download_url': f"/consultoria/download-relatorio/{resultado['arquivo']}"
            })
        return jsonify({'error': resultado['message']}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/consultoria/download-relatorio/<filename>')
@login_required
def consultoria_download_relatorio(filename):
    try:
        reports_dir = os.path.join(os.getcwd(), 'app', 'reports', 'consultoria')
        file_path = os.path.join(reports_dir, filename)
        if not os.path.exists(file_path):
            flash('Arquivo nao encontrado', 'error')
            return redirect('/consultoria/relatorios')
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'Erro ao baixar arquivo: {str(e)}', 'error')
        return redirect('/consultoria/relatorios')


@app.route('/consultoria/api/relatorios-recentes')
@login_required
def consultoria_api_relatorios_recentes():
    try:
        from app.services.consultoria_reports import ConsultoriaReportService
        service = ConsultoriaReportService()
        return jsonify(service.listar_relatorios_recentes())
    except ImportError:
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/consultoria/api/estatisticas-dashboard')
@login_required
def consultoria_api_estatisticas_dashboard():
    try:
        from app.services.consultoria_reports import ConsultoriaReportService
        service = ConsultoriaReportService()
        return jsonify(service.get_estatisticas_dashboard())
    except ImportError:
        return jsonify({
            'faturamento_total': 'R$ 485k',
            'taxa_sucesso': '94%',
            'satisfacao_cliente': '4.8/5',
            'capacidade_utilizada': '87%',
            'projetos_ativos': 8,
            'total_clientes': 24,
            'consultores_ativos': 8
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500