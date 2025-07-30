from flask import request
from flask_restx import Namespace, Resource

from obras.musicas.schemas.instrumento_schema import get_instrumento_schema
from obras.musicas.services.instrumento_service import InstrumentoService

instrumento_ns = Namespace('instrumentos', 'Gestão de instrumentos musicais')

instrumento_model, instrumento_input, instrumento_update = get_instrumento_schema(instrumento_ns)


@instrumento_ns.route("/musicais/instrumentos")
class InstrumentoBasic(Resource):

    @instrumento_ns.doc("list_instrumentos")
    @instrumento_ns.marshal_list_with(instrumento_model)
    def get(self):
        """ Lista todos os instrumentos """
        try:
            instrumentos = InstrumentoService.get_all_instrumentos()
            return [instrumento.to_dict() for instrumento in instrumentos]
        except Exception as e:
            instrumento_ns.abort(500, f"Erro ao obter instrumentos: {str(e)}")

    @instrumento_ns.doc('create_instrumento')
    @instrumento_ns.expect(instrumento_input, validate=True)
    @instrumento_ns.marshal_with(instrumento_model, code=201)
    def post(self):
        """Cria um novo instrumento"""
        data = request.get_json()

        if not data:
            instrumento_ns.abort(400, "No data provided")

        # Validate required fields
        if (not data.get('nome')
                or not data.get('grupo')):
            instrumento_ns.abort(400, "Campos não informados: (nome, grupo)")

        try:
            instrumento = InstrumentoService.create_instrumento(data)
            return instrumento.to_dict(), 201
        except ValueError as e:
            instrumento_ns.abort(400, str(e))
        except Exception as e:
            instrumento_ns.abort(500, str(e))


@instrumento_ns.route('/musicais/instrumento/<int:instrumento_id>')
@instrumento_ns.response(404, 'Instrumento não encontrado')
@instrumento_ns.param('instrumento_id', 'Identificador do instrumento')
class InstrumentoResource(Resource):

    @instrumento_ns.doc('get_instrumento')
    @instrumento_ns.marshal_with(instrumento_model)
    def get(self, instrumento_id):
        try:
            instrumento = InstrumentoService.get_instrumento_by_id(instrumento_id)
            if not instrumento:
                instrumento_ns.abort(404, f"Instrumento {instrumento_id} não encontrado")
            return instrumento.to_dict()
        except Exception as e:
            instrumento_ns.abort(500, f"Error ao recuperar instrumento {instrumento_id}: {str(e)}")

    @instrumento_ns.doc('update_instrumento')
    @instrumento_ns.expect(instrumento_update, validate=True)
    @instrumento_ns.marshal_with(instrumento_model)
    def put(self, instrumento_id):
        data = request.get_json()
        if not data:
            instrumento_ns.abort(400, "No data provided")

        try:
            instrumento = InstrumentoService.update_instrumento(instrumento_id, data)
            if not instrumento:
                instrumento_ns.abort(404, "Instrumento não encontrado")
            return instrumento.to_dict()
        except ValueError as e:
            instrumento_ns.abort(400, str(e))
        except Exception as e:
            instrumento_ns.abort(500, str(e))

    @instrumento_ns.doc('delete_instrumento')
    @instrumento_ns.response(204, 'Instrumento apagado')
    def delete(self, instrumento_id):
        try:
            deleted = InstrumentoService.delete_instrumento(instrumento_id)
            if not deleted:
                instrumento_ns.abort(404, "Instrumento não encontrado")
            return '', 204
        except Exception as e:
            instrumento_ns.abort(500, str(e))


@instrumento_ns.route('/musicais/instrumento/<grupo>/grupos')
@instrumento_ns.response(404, 'Instrumentos não encontrados')
@instrumento_ns.param('grupo', 'Grupo da instrumento')
class InstrumentoAdvancedResource(Resource):

    @instrumento_ns.doc('get_instrumentos_por_grupo')
    @instrumento_ns.marshal_list_with(instrumento_model)
    def get(self, grupo):
        try:
            instrumentos = InstrumentoService.get_instrumentos_by_grupo(grupo)
            if not instrumentos:
                instrumento_ns.abort(404, f"Não foram encontrados instrumentos para o grupo {grupo}")
            return [instrumento.to_dict() for instrumento in instrumentos]
        except Exception as e:
            instrumento_ns.abort(500, f"Error ao recuperar instrumento: {str(e)}")
