from flask_restx import fields


def get_instrumentacao_schema(api):
    instrumentacao_model = api.model('Instrumentacao', {
        'id': fields.Integer(readonly=True,
                             description='Identificacao do instrumentacao'),
        'id_instrumento': fields.String(required=True,
                                        description='Id do instrumento',
                                        example='1'),
        'id_composicao': fields.String(required=True,
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

    return instrumentacao_model, instrumentacao_input
