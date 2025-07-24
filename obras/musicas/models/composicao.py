from datetime import datetime

from infra import db


class Composicao(db.Model):
    """ Composicao entity """
    __tablename__ = 'composicao'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    data_composicao = db.Column(db.String(10), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    observacao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (f'<Composicao:: '
                f'id:{self.id}, '
                f'titulo:{self.titulo}, '
                f'data_composicao:{self.data_composicao}, '
                f'categoria:{self.categoria} '
                f'created_at: {self.created_at.isoformat() if self.created_at else None} ',
                f'updated_at: {self.updated_at.isoformat() if self.updated_at else None}>')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data_composicao': self.data_composicao,
            'categoria': self.categoria,
            'observacao': self.observacao,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create(self, titulo, data_composicao, categoria, numero_composicao, observacao=None):

        composicao = self(titulo=titulo,
                          data_composicao=data_composicao,
                          categoria=categoria,
                          observacao=observacao,
                          numero_composicao=numero_composicao)
        db.session.add(composicao)
        db.session.commit()
        return composicao

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(self, composicao_id):
        return self.query.get(composicao_id)

    @classmethod
    def get_by_data_and_categoria(self, data_composicao, categoria):
        return (self
                .query
                .filter_by(
                    data_composicao=data_composicao,
                    categoria=categoria)
                .first())

    @classmethod
    def get_all(self):
        return self.query.all()
