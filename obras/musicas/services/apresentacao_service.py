from infra import db
from obras.musicas.models.apresentacao import Apresentacao


class ApresentacaoService:
    """Service layer for user operations"""

    @staticmethod
    def get_apresentacao_by_id(id_apresentacao):
        return Apresentacao.get_by_id(id_apresentacao)

    @staticmethod
    def get_apresentacoes_by_composicao(id_composicao):
        return Apresentacao.get_by_id_composicao(id_composicao)

    @staticmethod
    def create_apresentacao(data):
        existing_apresentacao = Apresentacao.get_unique(data['evento'])
        if existing_apresentacao:
            raise ValueError(f"Ja existe apresentação para o evento {data['evento']}")

        if 'id_composicao' not in data:
            raise ValueError(f"A apresentação no evento {data['evento']} deve ser ligado à uma composição")

        apresentacoes = Apresentacao.get_by_id_composicao(id_composicao=data['id_composicao'])

        my_apresentacoes = [apresentacao.to_dict() for apresentacao in apresentacoes]
        has_estreia = any(my_apresentacao['is_estreia'] for my_apresentacao in my_apresentacoes)

        if has_estreia:
            raise ValueError(f"Já existe estreia para essa composição")

        try:
            return Apresentacao.create(
                id_composicao=data['id_composicao'],
                localidade=data['localidade'],
                local=data['local'],
                evento=data['evento'],
                data_evento=data['data_evento'],
                is_estreia=data['is_estreia'],
                url_evento=data['url_evento'])
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao criar apresentacao: {str(e)}")

    @staticmethod
    def update_apresentacao(id_apresentacao, data):
        apresentacao = Apresentacao.get_by_id(id_apresentacao)
        if not apresentacao:
            return None

        try:
            return apresentacao.update(**data)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar apresentação: {str(e)}")

    @staticmethod
    def delete_apresentacao(id_apresentacao):
        apresentacao = Apresentacao.get_by_id(id_apresentacao)
        if not apresentacao:
            return None

        try:
            apresentacao.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao apagar apresentação: {str(e)}")
