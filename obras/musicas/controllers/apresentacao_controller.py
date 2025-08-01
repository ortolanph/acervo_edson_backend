from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.apresentacao_schema import get_apresentacao_schema
from obras.musicas.services.apresentacao_service import ApresentacaoService

apresentacao_ns = Namespace('apresentacoes', 'Gestão de apresentações')

apresentacao_model, apresentacao_input, apresentcao_update = get_apresentacao_schema(apresentacao_ns)


@apresentacao_ns.route("/musicais/apresentacoes")
class ApresentacaoBasic(Resource):

    @apresentacao_ns.doc('create_apresentacao')
    @apresentacao_ns.expect(apresentacao_input, validate=True)
    @apresentacao_ns.marshal_list_with(apresentacao_model, code=201)
    def post(self):
        """Cria uma nova apresentação"""
        data = request.get_json()

        if not data:
            apresentacao_ns.abort(400, "No data provided")

        # Validate required fields
        if (not data.get('id_composicao')
                or not data.get('localidade')
                or not data.get('local')
                or not data.get('evento')
                or not data.get('data_evento')
                or not data.get('is_estreia')):
            apresentacao_ns.abort(400,
                                  "Campos não informados: (id_composicao, localidade, local, evento, data_evento, is_estreia)")

        try:
            apresentacao = ApresentacaoService.create_apresentacao(data)
            return apresentacao.to_dict(), 201
        except ValueError as e:
            apresentacao_ns.abort(400, str(e))
        except Exception as e:
            apresentacao_ns.abort(500, str(e))


@apresentacao_ns.route('/musicais/apresentacoes/<int:apresentacao_id>')
@apresentacao_ns.response(404, 'Apresentação não encontrada')
@apresentacao_ns.param('apresentacao_id', 'Identificador da apresentação')
class ApresentacaoResource(Resource):

    @apresentacao_ns.doc('get_apresentacao')
    @apresentacao_ns.marshal_with(apresentacao_model)
    def get(self, apresentacao_id):
        try:
            apresentacao = ApresentacaoService.get_apresentacao_by_id(apresentacao_id)
            if not apresentacao:
                apresentacao_ns.abort(404, f"Apresentação {apresentacao_id} não encontrada")
            return apresentacao.to_dict()
        except Exception as e:
            apresentacao_ns.abort(500, f"Error ao recuperar apresentação {apresentacao_id}: {str(e)}")

    # TODO: Se campo is_estreia vir como true, alterar o registro que tem como is_estreia = True para False
    @apresentacao_ns.doc('update_apresentacao')
    @apresentacao_ns.expect(apresentcao_update, validate=True)
    @apresentacao_ns.marshal_with(apresentacao_model)
    def put(self, apresentacao_id):
        data = request.get_json()
        if not data:
            apresentacao_ns.abort(400, "No data provided")

        try:
            apresentacao = ApresentacaoService.update_apresentacao(apresentacao_id, data)
            if not apresentacao:
                apresentacao_ns.abort(404, "Apresentação não encontrada")
            return apresentacao.to_dict()
        except ValueError as e:
            apresentacao_ns.abort(400, str(e))
        except Exception as e:
            apresentacao_ns.abort(500, str(e))

    @apresentacao_ns.doc('delete_apresentacao')
    @apresentacao_ns.response(204, 'Apresentação apagada')
    def delete(self, apresentacao_id):
        try:
            deleted = ApresentacaoService.delete_apresentacao(apresentacao_id)
            if not deleted:
                apresentacao_ns.abort(404, "Subtítulo não encontrado")
            return '', 204
        except Exception as e:
            apresentacao_ns.abort(500, str(e))


# TODO: Pendente de adicionar os intérpretes na resposta
@apresentacao_ns.route('/musicais/apresentacoes/<int:id_composicao>/composicao')
@apresentacao_ns.response(404, 'Apresentacões não encontradas')
@apresentacao_ns.param('id_composicao', 'Identificação da composição')
class ApresentacaoAdvancedResource(Resource):

    @apresentacao_ns.doc('get_all_apresentacoes_by_composicao')
    @apresentacao_ns.marshal_with(apresentacao_model)
    def get(self, id_composicao):
        try:
            apresentacoes = ApresentacaoService.get_apresentacoes_by_composicao(id_composicao)
            if not apresentacoes:
                apresentacao_ns.abort(404, f"Composição {id_composicao} não possui apresentações")
            return [apresentacao.to_dict() for apresentacao in apresentacoes]
        except Exception as e:
            apresentacao_ns.abort(500, f"Error ao recuperar composição: {str(e)}")
