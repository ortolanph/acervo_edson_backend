from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.composicao_schema import get_composicao_schema
from obras.musicas.services.composicao_service import ComposicaoService

composicao_ns = Namespace('composicoes', 'Gestão de composições')

composicao_model, composicao_input, composicao_update = get_composicao_schema(composicao_ns)


@composicao_ns.route("/musicais")
class ComposicaoBasic(Resource):

    @composicao_ns.doc("list_composicoes")
    @composicao_ns.marshal_list_with(composicao_model)
    def get(self):
        try:
            composicoes = ComposicaoService.get_all_composicoes()
            return [composicao.to_dict() for composicao in composicoes]
        except Exception as e:
            composicao_ns.abort(500, f"Error retrieving users: {str(e)}")

    @composicao_ns.doc('create_composicao')
    @composicao_ns.expect(composicao_input, validate=True)
    @composicao_ns.marshal_with(composicao_model, code=201)
    def post(self):
        """Cria uma nova composicao"""
        data = request.get_json()

        if not data:
            composicao_ns.abort(400, "No data provided")

        # Validate required fields
        if (not data.get('titulo')
                or not data.get('data_composicao')
                or not data.get('categoria')):
            composicao_ns.abort(400, "Campos não informados: (titulo, data_composicao, categoria)")

        try:
            composicao = ComposicaoService.create_composicao(data)
            return composicao.to_dict(), 201
        except ValueError as e:
            composicao_ns.abort(400, str(e))
        except Exception as e:
            composicao_ns.abort(500, str(e))


@composicao_ns.route('/musicais/<int:composicao_id>')
@composicao_ns.response(404, 'Composição não encontrada')
@composicao_ns.param('composicao_id', 'Identificador da composição')
class ComposicaoResource(Resource):
    @composicao_ns.doc('get_composicao')
    @composicao_ns.marshal_with(composicao_model)
    def get(self, composicao_id):
        try:
            composicao = ComposicaoService.get_composicao_by_id(composicao_id)
            if not composicao:
                composicao_ns.abort(404, f"Composição {composicao_id} não encontrada")
            return composicao.to_dict()
        except Exception as e:
            composicao_ns.abort(500, f"Error ao recuperar composição {composicao_id}: {str(e)}")

    @composicao_ns.doc('update_composicao')
    @composicao_ns.expect(composicao_update, validate=True)
    @composicao_ns.marshal_with(composicao_model)
    def put(self, composicao_id):
        data = request.get_json()
        if not data:
            composicao_ns.abort(400, "No data provided")

        try:
            composicao = ComposicaoService.update_composicao(composicao_id, data)
            if not composicao:
                composicao_ns.abort(404, "Composição não encontrada")
            return composicao.to_dict()
        except ValueError as e:
            composicao_ns.abort(400, str(e))
        except Exception as e:
            composicao_ns.abort(500, str(e))

    @composicao_ns.doc('delete_composicao')
    @composicao_ns.response(204, 'Composição apagada')
    def delete(self, composicao_id):
        try:
            deleted = ComposicaoService.delete_composicao(composicao_id)
            if not deleted:
                composicao_ns.abort(404, "Composição não encontrada")
            return '', 204
        except Exception as e:
            composicao_ns.abort(500, str(e))

@composicao_ns.route('/musicais/composicao/<data_composicao>/<categoria>')
@composicao_ns.response(404, 'Composição não encontrada')
@composicao_ns.param('identificacao_composicao', 'Identificação da composição')
class ComposicaoAdvancedResource(Resource):
    @composicao_ns.doc('get_composicao_by_data_and_categoria')
    @composicao_ns.marshal_with(composicao_model)
    def get(self, data_composicao, categoria):
        try:
            composicao = ComposicaoService.get_composicao_by_numero(data_composicao, categoria)
            if not composicao:
                composicao_ns.abort(404, f"Composição {data_composicao}/{categoria} não encontrada")
            return composicao.to_dict()
        except Exception as e:
            composicao_ns.abort(500, f"Error ao recuperar composição: {str(e)}")
