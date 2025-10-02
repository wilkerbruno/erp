from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.consultoria import bp
import os

@bp.route('/')
@login_required
def index():
    """Dashboard principal da consultoria"""
    return render_template('consultoria/index.html')

@bp.route('/projetos')
@login_required
def projetos():
    """Página de projetos"""
    return render_template('consultoria/projetos.html')

@bp.route('/clientes')
@login_required
def clientes():
    """Página de clientes"""
    return render_template('consultoria/clientes.html')

@bp.route('/consultores')
@login_required
def consultores():
    """Página de consultores"""
    return render_template('consultoria/consultores.html')

@bp.route('/contratos')
@login_required
def contratos():
    """Página de contratos"""
    return render_template('consultoria/contratos.html')

@bp.route('/cronogramas')
@login_required
def cronogramas():
    """Página de cronogramas"""
    return render_template('consultoria/cronogramas.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Página principal de relatórios"""
    print("DEBUG: Acessando página de relatórios")  # Debug
    try:
        return render_template('consultoria/relatorios.html')
    except Exception as e:
        print(f"ERRO: {e}")
        return f"Erro ao carregar template: {e}", 500

# APIs para Relatórios
@bp.route('/api/gerar-relatorio', methods=['POST'])
@login_required
def api_gerar_relatorio():
    """API para gerar relatórios"""
    try:
        # Importar aqui para evitar erro se não instalado
        try:
            from app.services.consultoria_reports import ConsultoriaReportService
        except ImportError:
            return jsonify({'error': 'Serviço de relatórios não instalado. Execute: pip install pandas openpyxl xlsxwriter reportlab matplotlib seaborn python-docx'}), 500
        
        data = request.get_json()
        
        tipo_relatorio = data.get('tipo')
        periodo = data.get('periodo')
        formato = data.get('formato', 'excel')
        filtros = data.get('filtros', {})
        
        if not tipo_relatorio:
            return jsonify({'error': 'Tipo de relatório é obrigatório'}), 400
        
        # Instanciar serviço de relatórios
        service = ConsultoriaReportService()
        
        # Gerar relatório baseado no tipo
        resultado = service.gerar_relatorio(
            tipo=tipo_relatorio,
            periodo=periodo,
            formato=formato,
            filtros=filtros,
            usuario=current_user.username if current_user.is_authenticated else 'Sistema'
        )
        
        if resultado['success']:
            return jsonify({
                'success': True,
                'message': 'Relatório gerado com sucesso!',
                'arquivo': resultado['arquivo'],
                'nome_arquivo': resultado['nome_arquivo'],
                'download_url': f"/consultoria/download-relatorio/{resultado['arquivo']}"
            })
        else:
            return jsonify({'error': resultado['message']}), 500
            
    except Exception as e:
        print(f"Erro na API gerar-relatorio: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@bp.route('/download-relatorio/<filename>')
@login_required 
def download_relatorio(filename):
    """Download de relatórios gerados"""
    try:
        reports_dir = os.path.join(os.getcwd(), 'app', 'reports', 'consultoria')
        file_path = os.path.join(reports_dir, filename)
        
        if not os.path.exists(file_path):
            flash('Arquivo não encontrado', 'error')
            return redirect(url_for('consultoria.relatorios'))
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        flash(f'Erro ao baixar arquivo: {str(e)}', 'error')
        return redirect(url_for('consultoria.relatorios'))

@bp.route('/api/relatorios-recentes')
@login_required
def api_relatorios_recentes():
    """API para listar relatórios recentes"""
    try:
        try:
            from app.services.consultoria_reports import ConsultoriaReportService
            service = ConsultoriaReportService()
            relatorios = service.listar_relatorios_recentes()
            return jsonify(relatorios)
        except ImportError:
            return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/estatisticas-dashboard')
@login_required
def api_estatisticas_dashboard():
    """API para estatísticas do dashboard"""
    try:
        try:
            from app.services.consultoria_reports import ConsultoriaReportService
            service = ConsultoriaReportService()
            stats = service.get_estatisticas_dashboard()
            return jsonify(stats)
        except ImportError:
            # Dados mockados se o serviço não estiver disponível
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

# Rota de teste para debug
@bp.route('/test')
def test():
    """Rota de teste"""
    return "Blueprint consultoria funcionando!"

# ===== NOVAS FUNCIONALIDADES =====

@bp.route('/diagnostico-efo')
@login_required
def diagnostico_efo():
    """Diagnóstico EFO - Empresarial, Financeiro e Operacional"""
    return render_template('consultoria/diagnostico_efo.html')

@bp.route('/diagnostico-inicial')
@login_required
def diagnostico_inicial():
    """Diagnóstico Inicial - Checklist de Avaliação"""
    return render_template('consultoria/diagnostico_inicial.html')

@bp.route('/checklist-sfm')
@login_required
def checklist_sfm():
    """Checklist SFM - Shop Floor Management"""
    return render_template('consultoria/checklist_sfm.html')

@bp.route('/acompanhamento')
@login_required
def acompanhamento():
    """Acompanhamento - Auditorias e Follow-up"""
    return render_template('consultoria/acompanhamento.html')
