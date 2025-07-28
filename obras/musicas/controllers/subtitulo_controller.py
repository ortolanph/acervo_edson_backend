from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.subtitulo_schema import get_subtitulo_schema
from obras.musicas.services.subtitulo_service import SubtituloService

subtitulo_ns = Namespace('subtitulos', 'Gestão de subtítulos')

subtitulo_model, subtitulo_input, subtitulo_update = get_subtitulo_schema(subtitulo_ns)


@subtitulo_ns.route("/musicais/subtitulos")
class SubtituloBasic(Resource):

    @subtitulo_ns.doc('create_subtitulo')
    @subtitulo_ns.expect(subtitulo_input, validate=True)
    @subtitulo_ns.marshal_with(subtitulo_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        if not data:
            subtitulo_ns.abort(400, "No data provided")

        # Validate required fields
        if (not data.get('id_composicao')
                or not data.get('subtitulo')
                or not data.get('lingua')):
            subtitulo_ns.abort(400, "Campos não informados: (id_composicao, subtitulo, lingua)")

        try:
            subtitulo = SubtituloService.create_subtitulo(data)
            return subtitulo.to_dict(), 201
        except ValueError as e:
            subtitulo_ns.abort(400, str(e))
        except Exception as e:
            subtitulo_ns.abort(500, str(e))


@subtitulo_ns.route('/musicais/subtitulos/<int:subtitulo_id>')
@subtitulo_ns.response(404, 'Subtítulo não encontrado')
@subtitulo_ns.param('subtitulo_id', 'Identificador do subtitulo')
class SubtituloResource(Resource):
    @subtitulo_ns.doc('get_subtitulo')
    @subtitulo_ns.marshal_with(subtitulo_model)
    def get(self, subtitulo_id):
        try:
            subtitulo = SubtituloService.get_subtitulo_by_id(subtitulo_id)
            if not subtitulo:
                subtitulo_ns.abort(404, f"Subtitulo {subtitulo_id} não encontrado")
            return subtitulo.to_dict()
        except Exception as e:
            subtitulo_ns.abort(500, f"Error ao recuperar subtítulo {subtitulo_id}: {str(e)}")

    @subtitulo_ns.doc('update_subtitulo')
    @subtitulo_ns.expect(subtitulo_update, validate=True)
    @subtitulo_ns.marshal_with(subtitulo_model)
    def put(self, subtitulo_id):
        data = request.get_json()
        if not data:
            subtitulo_ns.abort(400, "No data provided")

        try:
            subtitulo = SubtituloService.update_subtitulo(subtitulo_id, data)
            if not subtitulo:
                subtitulo_ns.abort(404, "Subtítulo não encontrado")
            return subtitulo.to_dict()
        except ValueError as e:
            subtitulo_ns.abort(400, str(e))
        except Exception as e:
            subtitulo_ns.abort(500, str(e))

    @subtitulo_ns.doc('delete_subtitulo')
    @subtitulo_ns.response(204, 'Subtítulo apagado')
    def delete(self, subtitulo_id):
        try:
            deleted = SubtituloService.delete_subtitulo(subtitulo_id)
            if not deleted:
                subtitulo_ns.abort(404, "Subtítulo não encontrado")
            return '', 204
        except Exception as e:
            subtitulo_ns.abort(500, str(e))


@subtitulo_ns.route('/musicais/subtitulos/<int:id_composicao>/composicao')
@subtitulo_ns.response(404, 'Subtítulos não encontrados')
@subtitulo_ns.param('id_composicao', 'Identificação da composição')
class SubtituloAdvancedResource(Resource):
    @subtitulo_ns.doc('get_all_subtitulos_by_composicao')
    @subtitulo_ns.marshal_with(subtitulo_model)
    def get(self, id_composicao):
        try:
            subtitulos = SubtituloService.get_subtitulos_by_composicao(id_composicao)
            if not subtitulos:
                subtitulo_ns.abort(404, f"Composição {id_composicao} não possui subtítulos")
            return subtitulos.to_dict()
        except Exception as e:
            subtitulo_ns.abort(500, f"Error ao recuperar composição: {str(e)}")
