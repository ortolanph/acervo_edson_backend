from flask_restx import fields


def get_subtitulo_schema(api):
    subtitulo_model = api.model('Subtitulo', {
        'id': fields.Integer(readonly=True,
                             description='Identificacao do subtitulo'),
        'id_composicao': fields.Integer(required=True,
                                        description='Identificacao da composicao associada',
                                        example="1"),
        'subtitulo': fields.String(required=True,
                                   description='Subtítulo da composição',
                                   example='A new Opera'),
        'lingua': fields.String(required=True,
                                description='A língua do subtítulo',
                                example='en-US'),
        'created_at': fields.DateTime(readonly=True,
                                      description='Creation timestamp',
                                      dt_format='iso8601'),
        'updated_at': fields.DateTime(readonly=True,
                                      description='Last update timestamp',
                                      dt_format='iso8601')
    })

    subtitulo_input = api.model('SubtituloInput', {
        'id_composicao': fields.Integer(required=True,
                                        description='Identificacao da composicao associada',
                                        example="1"),
        'subtitulo': fields.String(required=True,
                                   description='Subtítulo da composição',
                                   example='A new Opera'),
        'lingua': fields.String(required=True,
                                description='A língua do subtítulo',
                                example='en-US'),
    })

    subtitulo_update = api.model('SubtituloUpdate', {
        'id_composicao': fields.Integer(description='Identificacao da composicao associada',
                                        example="1"),
        'subtitulo': fields.String(description='Subtítulo da composição',
                                   example='A new Opera'),
        'lingua': fields.String(description='A língua do subtítulo',
                                example='en-US'),
    })

    return subtitulo_model, subtitulo_input, subtitulo_update
