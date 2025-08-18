from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SurveyForm
from .models import db, Cliente, Pesquisa, Resposta
from .email import send_survey_email
from .utils import calculate_nps

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/')
def index():
    # A simple homepage
    return render_template('index.html', title='Página Inicial')

@main_bp.route('/survey/<int:pesquisa_id>/<int:cliente_id>', methods=['GET', 'POST'])
def survey(pesquisa_id, cliente_id):
    pesquisa = Pesquisa.query.get_or_404(pesquisa_id)
    cliente = Cliente.query.get_or_404(cliente_id)

    form = SurveyForm()
    if form.validate_on_submit():
        # Check if this client has already responded to this survey
        existing_response = Resposta.query.filter_by(
            cliente_id=cliente.id,
            pesquisa_id=pesquisa.id
        ).first()

        if existing_response:
            flash('Você já respondeu a esta pesquisa.', 'info')
            return redirect(url_for('main_bp.thank_you'))

        resposta = Resposta(
            nota=form.score.data,
            comentario=form.comment.data,
            cliente_id=cliente.id,
            pesquisa_id=pesquisa.id
        )
        db.session.add(resposta)
        db.session.commit()
        flash('Obrigado por sua resposta!', 'success')
        return redirect(url_for('main_bp.thank_you'))

    return render_template('survey.html', title=pesquisa.nome, form=form, pesquisa=pesquisa)

@main_bp.route('/thank-you')
def thank_you():
    return render_template('thank_you.html', title='Obrigado!')

# --- Admin / Test Routes ---
@main_bp.route('/send-survey/<int:pesquisa_id>')
def send_survey(pesquisa_id):
    """
    Action to send a survey to all clients.
    In a real app, this should be a background task.
    """
    pesquisa = Pesquisa.query.get_or_404(pesquisa_id)
    clientes = Cliente.query.all()

    if not clientes:
        flash('Nenhum cliente cadastrado para enviar a pesquisa.', 'warning')
        return redirect(url_for('main_bp.index'))

    for cliente in clientes:
        send_survey_email(cliente, pesquisa)

    flash(f"A pesquisa '{pesquisa.nome}' foi enviada para {len(clientes)} cliente(s).", 'success')
    return redirect(url_for('main_bp.index'))

# --- Dashboard Routes ---
@main_bp.route('/dashboard')
def dashboard():
    """Mostra uma lista de todas as pesquisas."""
    pesquisas = Pesquisa.query.order_by(Pesquisa.data_criacao.desc()).all()
    return render_template('dashboard.html', title='Dashboard', pesquisas=pesquisas)

@main_bp.route('/dashboard/survey/<int:pesquisa_id>')
def survey_results(pesquisa_id):
    """Mostra os resultados detalhados de uma pesquisa."""
    pesquisa = Pesquisa.query.get_or_404(pesquisa_id)
    results = calculate_nps(pesquisa)
    return render_template('survey_results.html', title=f"Resultados de {pesquisa.nome}", pesquisa=pesquisa, results=results)
