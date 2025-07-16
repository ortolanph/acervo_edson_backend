from flask import Blueprint, jsonify, request

from infra import db
from obras.musicais.models.composicao_musical import ComposicaoMusical

composicoes_bp = Blueprint('composicoes_musicais', __name__)


@composicoes_bp.route('/obras/musicais/composicoes', methods=['GET'])
def get_all_musical_composition():
    """Get all musical instruments"""
    try:
        composicoes = ComposicaoMusical.query.all()
        return jsonify([composicao.to_dict() for composicao in composicoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@composicoes_bp.route('/obras/musicais/composicoes', methods=['POST'])
def create_musical_composition():
    """Create a new musical instrument"""
    data = request.get_json()

    if (not data or
            'titulo' not in data or
            'data_composicao' not in data or
            'categoria' not in data):
        return jsonify({'error': 'Informações obrigatórias da composição musical não informadas: titulodata da composição e categoria'}), 400

    existing_composition = ComposicaoMusical.query.filter(
        (ComposicaoMusical.nome == data['titulo'])
    ).first()

    if existing_composition:
        return jsonify({'error': 'Composição musical já existe'}), 400

    try:
        composicao_musical = ComposicaoMusical(
            titulo=data['titulo'],
            data_composicao=data['data_composicao'],
            catgoria=data['categoria'],
            numero_composicao = f"{data['data_composicao']/data['categoria']}"
        )
        db.session.add(composicao_musical)
        db.session.commit()
        return jsonify(composicao_musical.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
