from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.composicao_schema import get_composicao_schema
from obras.musicas.schemas.instrumentacao_schema import get_instrumentacao_schema
from obras.musicas.services.composicao_service import ComposicaoService
from obras.musicas.services.instrumentacao_service import InstrumentacaoService

instrumentacao_ns = Namespace('instrumentacao', 'Gestão de instrumentações')

instrumentacao_model, instrumentacao_input = get_instrumentacao_schema(instrumentacao_ns)


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


@instrumentacao_ns.route('/musicais/instrumentacao/<int:composicao_id>')
@instrumentacao_ns.response(404, 'Composição não encontrada')
@instrumentacao_ns.param('composicao_id', 'Identificador da composição')
class ComposicaoResource(Resource):
    @instrumentacao_ns.doc('get_composicao')
    @instrumentacao_ns.marshal_with(instrumentacao_model)
    def get(self, composicao_id):
        try:
            composicao = ComposicaoService.get_composicao_by_id(composicao_id)
            if not composicao:
                instrumentacao_ns.abort(404, f"Composição {composicao_id} não encontrada")
            return composicao.to_dict()
        except Exception as e:
            instrumentacao_ns.abort(500, f"Error ao recuperar composição {composicao_id}: {str(e)}")

    @instrumentacao_ns.doc('update_composicao')
    @instrumentacao_ns.expect(composicao_update, validate=True)
    @instrumentacao_ns.marshal_with(instrumentacao_model)
    def put(self, composicao_id):
        data = request.get_json()
        if not data:
            instrumentacao_ns.abort(400, "No data provided")

        try:
            composicao = ComposicaoService.update_composicao(composicao_id, data)
            if not composicao:
                instrumentacao_ns.abort(404, "Composição não encontrada")
            return composicao.to_dict()
        except ValueError as e:
            instrumentacao_ns.abort(400, str(e))
        except Exception as e:
            instrumentacao_ns.abort(500, str(e))

    @instrumentacao_ns.doc('delete_composicao')
    @instrumentacao_ns.response(204, 'Composição apagada')
    def delete(self, composicao_id):
        try:
            deleted = ComposicaoService.delete_composicao(composicao_id)
            if not deleted:
                instrumentacao_ns.abort(404, "Composição não encontrada")
            return '', 204
        except Exception as e:
            instrumentacao_ns.abort(500, str(e))


@instrumentacao_ns.route('/musicais/composicao/<data_composicao>/<categoria>')
@instrumentacao_ns.response(404, 'Composição não encontrada')
@instrumentacao_ns.param('identificacao_composicao', 'Identificação da composição')
class ComposicaoAdvancedResource(Resource):
    @instrumentacao_ns.doc('get_composicao_by_data_and_categoria')
    @instrumentacao_ns.marshal_with(instrumentacao_model)
    def get(self, data_composicao, categoria):
        try:
            composicao = ComposicaoService.get_composicao_by_numero(data_composicao, categoria)
            if not composicao:
                instrumentacao_ns.abort(404, f"Composição {data_composicao}/{categoria} não encontrada")
            return composicao.to_dict()
        except Exception as e:
            instrumentacao_ns.abort(500, f"Error ao recuperar composição: {str(e)}")
