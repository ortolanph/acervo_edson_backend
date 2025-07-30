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
        instrumentations = Instrumentacao.get_all_instrumentos_by_composicao(id_composicao)

        my_instrumentations = [instrumentation.to_dict() for instrumentation in instrumentations ]

        instruments = []
        for instrumentation in my_instrumentations:
            instrument = Instrumento.get_by_id(instrumentation['id_instrumento']).to_dict()

            print(instrument)

            if instrument:
                instruments.append({
                    'id_instrumentacao': instrumentation['id'],
                    'id_instrumento': instrument['id'],
                    'nome': instrument['nome'],
                    'grupo': instrument['grupo'],
                })

        print(instruments)

        return instruments

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
