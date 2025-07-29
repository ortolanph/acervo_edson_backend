from infra import db
from obras.musicas.models.instrumento import Instrumento


class InstrumentoService:
    """Service layer for user operations"""

    @staticmethod
    def get_all_instrumentos():
        """Get all users"""
        return Instrumento.get_all()

    @staticmethod
    def get_instrumento_by_id(instrumento_id):
        return Instrumento.get_by_id(instrumento_id)

    @staticmethod
    def get_instrumento_by_nome(nome_instrumento):
        return Instrumento.get_by_nome(nome_instrumento)

    @staticmethod
    def get_instrumentos_by_grupo(grupo_instrumento):
        return Instrumento.get_by_grupo(grupo_instrumento)

    @staticmethod
    def create_instrumento(data):
        existing_instrumento = Instrumento.get_by_nome(data['nome'])
        if existing_instrumento:
            raise ValueError(f"Ja existe instrumento {data['nome']}")

        if 'grupo' not in data:
            raise ValueError(f"O instrumento {data['nome']} deve pertencer à um grupo")

        try:
            return Instrumento.create(
                nome=data['nome'],
                grupo=data['grupo'],
            )
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar instrumento: {str(e)}")

    @staticmethod
    def update_instrumento(id_instrumento, data):
        instrumento = Instrumento.get_by_id(id_instrumento)
        if not instrumento:
            return None

        try:
            return instrumento.update(**data)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar instrumento: {str(e)}")

    @staticmethod
    def delete_instrumento(id_instrumento):
        instrumento = Instrumento.get_by_id(id_instrumento)
        if not instrumento:
            return None

        try:
            instrumento.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao apagar instrumento: {str(e)}")
