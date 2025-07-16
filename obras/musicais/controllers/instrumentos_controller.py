from flask import jsonify, Blueprint, request

from infra import db
from obras.musicais.models.instrumento_musical import InstrumentoMusical

instrumentos_bp = Blueprint('instrumentos_musicais', __name__)


@instrumentos_bp.route('/obras/musicais/instrumentos', methods=['GET'])
def get_all_musical_instrument():
    """Get all musical instruments"""
    try:
        instrumentos = InstrumentoMusical.query.all()
        return jsonify([instrumento.to_dict() for instrumento in instrumentos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instrumentos_bp.route('/obras/musicais/instrumentos', methods=['POST'])
def create_instrument():
    """Create a new musical instrument"""
    data = request.get_json()

    if not data or 'nome' not in data or 'grupo' not in data:
        return jsonify({'error': 'Informações obrigatórias de instrumento musical não informadas: nome e grupo'}), 400

    existing_instrument = InstrumentoMusical.query.filter(
        (InstrumentoMusical.nome == data['nome']) | (InstrumentoMusical.grupo == data['grupo'])
    ).first()

    if existing_instrument:
        return jsonify({'error': 'Instrumento musical já existe'}), 400

    try:
        instrumento_musical = InstrumentoMusical(nome=data['nome'], grupo=data['grupo'])
        db.session.add(instrumento_musical)
        db.session.commit()
        return jsonify(instrumento_musical.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@instrumentos_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['GET'])
def get_musical_instrument_by_id(instrumento_id):
    """Get a specific user by ID"""
    try:
        instrumento_musical = InstrumentoMusical.query.get_or_404(instrumento_id)
        return jsonify(instrumento_musical.to_dict())
    except Exception as e:
        return jsonify({'error': 'Instrumento não encontrado'}), 404


@instrumentos_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['PUT'])
def update_instrument(user_id):
    """Update a user"""
    try:
        instrumento = InstrumentoMusical.query.get_or_404(user_id)
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Não foram encontradas alterações'}), 400

        InstrumentoMusical.nome = data['nome'] if 'nome' in data else InstrumentoMusical.nome
        InstrumentoMusical.grupo = data['grupo'] if 'grupo' in data else InstrumentoMusical.grupo

        db.session.commit()
        return jsonify(instrumento.to_dict())
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'error': str(e)}), 500


@instrumentos_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['DELETE'])
def delete_instrument(instrumento_id):
    """Delete a user"""
    try:
        instrumento = InstrumentoMusical.query.get_or_404(instrumento_id)
        db.session.delete(instrumento)
        db.session.commit()
        return jsonify({'message': 'Instrumento apagado com sucesso'})
    except Exception as e:
        db.session.rollback()
        if 'not found' in str(e).lower():
            return jsonify({'error': 'Instrumento não encontrado'}), 404
        return jsonify({'error': str(e)}), 500
