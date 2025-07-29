from flask_restx import fields


def get_instrumento_schema(api):
    instrumento_model = api.model('Instrumento', {
        'id': fields.Integer(readonly=True,
                             description='Identificacao do instrumento'),
        'nome': fields.String(required=True,
                              description='Nome do instrumento',
                              example='Violino'),
        'grupo': fields.String(required=True,
                               description='Grupo do instrumento',
                               example='Cordas'),
        'created_at': fields.DateTime(readonly=True,
                                      description='Creation timestamp',
                                      dt_format='iso8601'),
        'updated_at': fields.DateTime(readonly=True,
                                      description='Last update timestamp',
                                      dt_format='iso8601')
    })

    intrumento_input = api.model('InstrumentoInput', {
        'nome': fields.String(required=True,
                              description='Nome do instrumento',
                              example='Violino'),
        'grupo': fields.String(required=True,
                               description='Grupo do instrumento',
                               example='Cordas'),
    })

    instrumento_update = api.model('InstrumentoUpdate', {
        'nome': fields.String(description='Nome do instrumento',
                              example='Violino'),
        'grupo': fields.String(description='Grupo do instrumento',
                               example='Cordas'),
    })

    return instrumento_model, intrumento_input, instrumento_update
