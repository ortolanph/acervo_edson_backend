from flask import jsonify, Blueprint

from infra import db

general_bp = Blueprint('general_info', __name__)


@general_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return (
        jsonify(
            {
                'status': 'healthy',
                'message': 'API is running',
                'database_status': 'OK' if db else 'KO'
            }
        )
    )
