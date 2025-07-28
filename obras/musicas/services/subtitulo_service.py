from infra import db
from obras.musicas.models.subtitulo import Subtitulo


class SubtituloService:
    """Service layer for user operations"""

    @staticmethod
    def get_subtitulo_by_id(subtitulo_id):
        return Subtitulo.get_by_id(subtitulo_id)

    @staticmethod
    def get_subtitulos_by_composicao(composicao_id):
        return Subtitulo.get_by_composicao_id(composicao_id)

    @staticmethod
    def create_subtitulo(data):
        existing_subtitle = Subtitulo.get_by_subtitulo(data['subtitulo'])
        if existing_subtitle:
            raise ValueError(f"Ja existe subtitulo {data['subtitulo']}")

        if 'id_composicao' not in data:
            raise ValueError(f"O subtitulo {data['subtitulo']} deve ser ligado à uma composição")

        try:
            return Subtitulo.create(
                id_composicao=data['id_composicao'],
                subtitulo=data['subtitulo'],
                lingua=data['lingua'],
            )
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar subitulo: {str(e)}")

    @staticmethod
    def update_subtitulo(id_subtitulo, data):
        subtitulo = Subtitulo.get_by_id(id_subtitulo)
        if not subtitulo:
            return None

        try:
            return subtitulo.update(**data)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar subtitulo: {str(e)}")

    @staticmethod
    def delete_subtitulo(id_subtitulo):
        subtitulo = Subtitulo.get_by_id(id_subtitulo)
        if not subtitulo:
            return None

        try:
            subtitulo.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao apagar subtítulo: {str(e)}")
