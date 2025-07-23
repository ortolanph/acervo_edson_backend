from flask_restx import fields


def get_composicao_schema(api):
    composicao_model = api.model('Composicao', {
        'id': fields.Integer(readonly=True,
                             description='Identificacao interna da composição'),
        'titulo': fields.String(required=True,
                                description='Título da composição',
                                example='Orquestra para cordas #1'),
        'numero_composicao': fields.String(required=True,
                                           description='Número da composição',
                                           example='2025-01-22/Orquestra'),
        'data_composicao': fields.String(required=True,
                                       description='Data que a obra musical foi composta',
                                       example="2025-03-05"),
        'categoria': fields.String(required=True,
                                   description='Categoria da composição, pode ser Orquestra, Múisica de Câmara ou Música Vocal',
                                   example='Orquestra'),
        'observacao': fields.String(description='Observação pertinente à obra',
                                    example="PROTEGIDA POR DIREITOS AUTORAIS"),
        'created_at': fields.DateTime(readonly=True,
                                      description='Creation timestamp',
                                      dt_format='iso8601'),
        'updated_at': fields.DateTime(readonly=True,
                                      description='Last update timestamp',
                                      dt_format='iso8601')
    })

    composicao_input = api.model('ComposicaoInput', {
        'titulo': fields.String(required=True,
                                description='Título da composição',
                                example='Orquestra para cordas #1'),
        'data_composicao': fields.String(required=True,
                                       description='Data que a obra musical foi composta',
                                       example="2025-03-05"),
        'categoria': fields.String(required=True,
                                   description='Categoria da composição, pode ser Orquestra, Múisica de Câmara ou Música Vocal',
                                   example='Orquestra'),
        'observacao': fields.String(description='Observação pertinente à obra',
                                    example="PROTEGIDA POR DIREITOS AUTORAIS"),
    })

    composicao_update = api.model('ComposicaoUpdate', {
        'titulo': fields.String(description='Título da composição',
                                example='Orquestra para cordas #1'),
        'data_composicao': fields.String(description='Data que a obra musical foi composta',
                                       example="2025-03-05"),
        'categoria': fields.String(
            description='Categoria da composição, pode ser Orquestra, Múisica de Câmara ou Música Vocal',
            example='Orquestra'),
        'observacao': fields.String(description='Observação pertinente à obra',
                                    example="PROTEGIDA POR DIREITOS AUTORAIS"),
    })

    return composicao_model, composicao_input, composicao_update
