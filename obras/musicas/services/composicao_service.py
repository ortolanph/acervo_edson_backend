from infra import db
from obras.musicas.models.composicao import Composicao


class ComposicaoService:
    """Service layer for user operations"""

    @staticmethod
    def get_all_composicoes():
        """Get all users"""
        return Composicao.get_all()

    @staticmethod
    def get_composicao_by_id(composicao_id):
        return Composicao.get_by_id(composicao_id)

    @staticmethod
    def get_composicao_by_numero(data_composicao, categoria):
        return Composicao.get_by_data_and_categoria(data_composicao, categoria)

    @staticmethod
    def create_composicao(data):
        existing_composicao = Composicao.get_by_data_and_categoria(data['data_composicao'], data['categoria'])
        if existing_composicao:
            raise ValueError(f"Ja existe composicao {data['data_composicao']/data['categoria']}")

        try:
            return Composicao.create(
                titulo=data['titulo'],
                data_composicao=data['data_composicao'],
                categoria=data['categoria'],
                observacao=data['observacao'],
            )
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar composicao: {str(e)}")

    @staticmethod
    def update_composicao(composicao_id, data):
        """Update user with validation"""
        composicao = Composicao.get_by_id(composicao_id)
        if not composicao:
            return None

        try:
            return composicao.update(**data)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar composicao: {str(e)}")

    @staticmethod
    def delete_composicao(composicao_id):
        """Delete user"""
        composicao = Composicao.get_by_id(composicao_id)
        if not composicao:
            return False

        try:
            composicao.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao apagar composição: {str(e)}")
