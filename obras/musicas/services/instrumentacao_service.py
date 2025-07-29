from infra import db
from obras.musicas.models.instrumentacao import Instrumentacao
from obras.musicas.models.instrumento import Instrumento


class InstrumentacaoService:
    """Service layer for user operations"""

    @staticmethod
    def get_instrumentacao_by_id(instrumentacao_id):
        return Instrumentacao.get_by_id(instrumentacao_id)

    @staticmethod
    def get_instrumentacao_by_composicao(id_composicao):
        instrumentation = Instrumentacao.get_all_instrumentos_by_composicao(id_composicao)

        instruments = []
        for instrument in instrumentation:
            my_instrument = Instrumento.get_by_id(instrument['id_instrumento'])

            if my_instrument is not None:
                instruments.append(my_instrument)

        return [instrument.to_dict() for instrument in instruments]

    @staticmethod
    def create_instrumentacao(data):
        existing_instrumentacao = Instrumentacao.get_by_id_instrumento_and_id_composicao(data['id_instrumento'],
                                                                                         data['id_composicao'])
        if existing_instrumentacao:
            raise ValueError(f"Ja existe instrumentação para esta composição")

        try:
            return Instrumentacao.create(
                id_instrumento=data['id_instrumento'],
                id_composicao=data['id_composicao']
            )
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar instrumentacao: {str(e)}")

    @staticmethod
    def delete_instrumentacao(id_instrumentacao):
        """Delete user"""
        instrumentacao = Instrumentacao.get_by_id(id_instrumentacao)
        if not instrumentacao:
            return False

        try:
            instrumentacao.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao apagar instrumentação: {str(e)}")
