from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.instrumentacao_schema import get_instrumentacao_schema
from obras.musicas.services.instrumentacao_service import InstrumentacaoService

instrumentacao_ns = Namespace('instrumentacao', 'Gestão de instrumentações')

instrumentacao_model, instrumentacao_input, instrumentacao_output = get_instrumentacao_schema(instrumentacao_ns)


@instrumentacao_ns.route("/musicais/instrumenstacao")
class InstrumentacaoBasic(Resource):

    @instrumentacao_ns.doc('create_instrumentacao')
    @instrumentacao_ns.expect(instrumentacao_input, validate=True)
    @instrumentacao_ns.marshal_with(instrumentacao_model, code=201)
    def post(self):
        """Cria uma nova instrumentação"""
        data = request.get_json()

        if not data:
            instrumentacao_ns.abort(400, "No data provided")

        # Validate required fields
        if (data.get('id_composicao')
                or not data.get('id_instrunento')):
            instrumentacao_ns.abort(400, "Campos não informados: (id_composicao, id_instrunento)")

        try:
            instrumentacao = InstrumentacaoService.create_instrumentacao(data)
            return instrumentacao.to_dict(), 201
        except ValueError as e:
            instrumentacao_ns.abort(400, str(e))
        except Exception as e:
            instrumentacao_ns.abort(500, str(e))


@instrumentacao_ns.route('/musicais/instrumentacao/<int:instrumentacao_id>')
@instrumentacao_ns.response(404, 'Instrumentação não encontrada')
@instrumentacao_ns.param('composicao_id', 'Identificador da instrumentação')
class InstrumentacaoResource(Resource):

    @instrumentacao_ns.doc('get_instrumentacao')
    @instrumentacao_ns.marshal_with(instrumentacao_model)
    def get(self, instrumentacao_id):
        try:
            instrumentacao = InstrumentacaoService.get_instrumentacao_by_id(instrumentacao_id)
            if not instrumentacao:
                instrumentacao_ns.abort(404, f"Instrumentação {instrumentacao_id} não encontrada")
            return instrumentacao.to_dict()
        except Exception as e:
            instrumentacao_ns.abort(500, f"Error ao recuperar composição {instrumentacao_id}: {str(e)}")

    @instrumentacao_ns.doc('delete_instrumentacao')
    @instrumentacao_ns.response(204, 'Instrumentacao apagada')
    def delete(self, instrumentacao_id):
        try:
            deleted = InstrumentacaoService.delete_instrumentacao(instrumentacao_id)
            if not deleted:
                instrumentacao_ns.abort(404, "Composição não encontrada")
            return '', 204
        except Exception as e:
            instrumentacao_ns.abort(500, str(e))


@instrumentacao_ns.route('/musicais/instrumentacao/<int:id_composicao>/composicao')
@instrumentacao_ns.response(404, 'Composição não encontrada')
@instrumentacao_ns.param('identificacao_composicao', 'Identificação da composição')
class ComposicaoAdvancedResource(Resource):

    @instrumentacao_ns.doc('get_instrumentacao_by_categoria_id')
    @instrumentacao_ns.marshal_list_with(instrumentacao_output)
    def get(self, id_composicao):
        try:
            instrumentacoes = InstrumentacaoService.get_instrumentacao_by_composicao(id_composicao)
            if not instrumentacoes:
                instrumentacao_ns.abort(404, f"Não foi encontrada instrumentação para composição {id_composicao}")
            return [instrumentacao.to_dict() for instrumentacao in instrumentacoes]
        except Exception as e:
            instrumentacao_ns.abort(500, f"Error ao recuperar instrumentacao: {str(e)}")
