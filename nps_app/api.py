from flask import Blueprint, jsonify, request
from .models import db, Cliente, Pesquisa, Resposta
from .utils import calculate_nps

api_bp = Blueprint('api_bp', __name__, url_prefix='/api/v1')

@api_bp.route('/hello')
def hello_api():
    """Um endpoint de teste para a API."""
    return jsonify({"message": "Bem-vindo à API do NPS!"})

@api_bp.route('/customers', methods=['POST'])
def create_customer():
    """Endpoint para criar um novo cliente."""
    data = request.get_json()
    if not data or not 'email' in data:
        return jsonify({'error': 'Email é obrigatório'}), 400

    if Cliente.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Cliente com este email já existe'}), 409

    new_customer = Cliente(email=data['email'], nome=data.get('nome'))
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'Cliente criado com sucesso', 'id': new_customer.id}), 201

@api_bp.route('/surveys', methods=['POST'])
def create_survey():
    """Endpoint para criar uma nova pesquisa."""
    data = request.get_json()
    if not data or not 'nome' in data:
        return jsonify({'error': 'Nome da pesquisa é obrigatório'}), 400

    new_survey = Pesquisa(nome=data['nome'], descricao=data.get('descricao'))
    db.session.add(new_survey)
    db.session.commit()

    return jsonify({'message': 'Pesquisa criada com sucesso', 'id': new_survey.id}), 201

@api_bp.route('/surveys/<int:pesquisa_id>/results', methods=['GET'])
def get_survey_results(pesquisa_id):
    """Endpoint para obter os resultados de uma pesquisa."""
    pesquisa = Pesquisa.query.get_or_404(pesquisa_id)

    # Calcula as métricas usando a função helper
    results = calculate_nps(pesquisa)

    # Adiciona os dados da pesquisa e as respostas detalhadas
    results['pesquisa_id'] = pesquisa.id
    results['pesquisa_nome'] = pesquisa.nome
    results['respostas'] = [
        {
            'id': r.id,
            'nota': r.nota,
            'comentario': r.comentario,
            'data_resposta': r.data_resposta.isoformat()
        } for r in pesquisa.respostas
    ]

    return jsonify(results)
