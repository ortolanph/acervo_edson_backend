# from flask import jsonify, request
from flask import jsonify, Blueprint

# from obras.musicais.models.instrumento_musical import InstrumentoMusical, db
from obras.musicais.models.instrumento_musical import InstrumentoMusical

instrumentos_bp = Blueprint('instrumentos_musicais', __name__)


@instrumentos_bp.route('/obras/musicais/instrumentos', methods=['GET'])
def get_musical_instrument():
    """Get all users"""
    try:
        instrumentos = InstrumentoMusical.query.all()
        return jsonify([user.to_dict() for user in instrumentos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @im_bp.route('/obras/musicais/instrumentos', methods=['POST'])
# def create_user():
#     """Create a new user"""
#     data = request.get_json()
#
#     if not data or 'nome' not in data or 'grupo' not in data:
#         return jsonify({'error': 'Nome do Instrumento and Grupo are required'}), 400
#
#     # Check if user already exists
#     existing_user = InstrumentoMusical.query.filter(
#         (InstrumentoMusical.nome == data['nome']) | (InstrumentoMusical.grupo == data['grupo'])
#     ).first()
#
#     if existing_user:
#         return jsonify({'error': 'Instrumento musical já existe'}), 400
#
#     try:
#         instrumento_musical = InstrumentoMusical(nome=data['nome'], grupo=data['grupo'])
#         db.session.add(instrumento_musical)
#         db.session.commit()
#         return jsonify(instrumento_musical.to_dict()), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500
#
#
# @im_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['GET'])
# def get_user(instrumento_id):
#     """Get a specific user by ID"""
#     try:
#         user = InstrumentoMusical.query.get_or_404(instrumento_id)
#         return jsonify(user.to_dict())
#     except Exception as e:
#         return jsonify({'error': 'Instrumento não encontrado'}), 404
#
#
# @im_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['PUT'])
# def update_instrument(user_id):
#     """Update a user"""
#     try:
#         instrumento = InstrumentoMusical.query.get_or_404(user_id)
#         data = request.get_json()
#
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400
#
#         if 'nome' in data:
#             existing_user = InstrumentoMusical.query.filter(
#                 InstrumentoMusical.nome == data['nome'],
#                 InstrumentoMusical.id != user_id
#             ).first()
#             if existing_user:
#                 return jsonify({'error': 'Já existe instrumento'}), 400
#             instrumento.username = data['nome']
#
#         if 'grupo' in data:
#             existing_user = InstrumentoMusical.query.filter(
#                 InstrumentoMusical.email == data['grupo'],
#                 InstrumentoMusical.id != user_id
#             ).first()
#             if existing_user:
#                 return jsonify({'error': 'Grupo já existe already exists'}), 400
#             instrumento.email = data['grupo']
#
#         db.session.commit()
#         return jsonify(instrumento.to_dict())
#     except Exception as e:
#         db.session.rollback()
#         if 'not found' in str(e).lower():
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify({'error': str(e)}), 500
#
#
# @im_bp.route('/obras/musicais/instrumentos/<int:instrumento_id>', methods=['DELETE'])
# def delete_instrument(instrumento_id):
#     """Delete a user"""
#     try:
#         instrumento = InstrumentoMusical.query.get_or_404(instrumento_id)
#         db.session.delete(instrumento)
#         db.session.commit()
#         return jsonify({'message': 'Instrumento apagado com sucesso'})
#     except Exception as e:
#         db.session.rollback()
#         if 'not found' in str(e).lower():
#             return jsonify({'error': 'Instrumento não encontrado'}), 404
#         return jsonify({'error': str(e)}), 500
