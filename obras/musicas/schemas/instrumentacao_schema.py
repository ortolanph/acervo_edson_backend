from flask_restx import fields


def get_instrumentacao_schema(api):
    instrumentacao_model = api.model('Instrumentacao', {
        'id': fields.Integer(readonly=True,
                             description='Identificacao do instrumentacao'),
        'id_instrumento': fields.Integer(required=True,
                                         description='Id do instrumento',
                                         example='1'),
        'id_composicao': fields.Integer(required=True,
                                        description='Id da composição',
                                        example='2'),
        'created_at': fields.DateTime(readonly=True,
                                      description='Creation timestamp',
                                      dt_format='iso8601'),
        'updated_at': fields.DateTime(readonly=True,
                                      description='Last update timestamp',
                                      dt_format='iso8601')
    })

    instrumentacao_input = api.model('InstrumentacaoInput', {
        'id_instrumento': fields.String(required=True,
                                        description='Id do instrumento',
                                        example='1'),
        'id_composicao': fields.String(required=True,
                                       description='Id da composição',
                                       example='2'),
    })

    instrumentacao_output = api.model('InstrumentacaoOutput', {
        'id_instrumentacao': fields.Integer(description='Id da instrumentacao'),
        'id_instrumento': fields.Integer(description='Id do instrumento',
                                         example='1'),
        'nome_instrumento': fields.String(description='Nome do instrumento',
                                          example='Violino'),
        'grupo_instrumento': fields.String(description='Grupo do instrumento')
    })

    return instrumentacao_model, instrumentacao_input, instrumentacao_output
