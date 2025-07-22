from flask_restx import fields


def get_composicao_schema(api):
    return api.model('Composicao', {
        'id': fields.Integer(readonly=True, description='Identificacao interna da composição'),
        'titulo': fields.String(required=True, description='Título da composição', example='Orquestra para cordas'),
        'numero_composicao': fields.String(required=True, description='Número da composição', example='2025-01-22/Orquestra'),
        'data_composicao': fields.Date(readonly=True, description='Data que a obra musical foi composta'),
        'categoria': fields.String(required=True, description='Categoria da composição, pode ser Orquestra, Múisica de Câmara ou Música Vocal', example='Orquestra'),
        'observacao': fields.String(readonly=True, description='Observação pertinente à obra'),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })
