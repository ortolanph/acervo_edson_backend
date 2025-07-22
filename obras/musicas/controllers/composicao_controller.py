from flask_restx import Namespace, Resource

from obras.musicas.schemas.composicao_schema import get_composicao_schema
from obras.musicas.services.composicao_service import ComposicaoService

composicao_ns = Namespace('composicoes', 'Gestão de composições')

composicao_model = get_composicao_schema(composicao_ns)


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
