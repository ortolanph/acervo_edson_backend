from datetime import datetime

from infra import db


class Instrumentacao(db.Model):
    """ Instrumentação entity """
    __tablename__ = 'instrumentacao'

    id = db.Column(db.Integer, primary_key=True)
    id_instrumento = db.Column(db.Integer, nullable=False)
    id_composicao = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (f'<Instrumentação:: '
                f'id:{self.id}, '
                f'id_instrumento:{self.id_instrumento}, '
                f'id_composicao:{self.id_composicao} '
                f'created_at: {self.created_at.isoformat() if self.created_at else None} ',
                f'updated_at: {self.updated_at.isoformat() if self.updated_at else None}>')

    def to_dict(self):
        return {
            'id': self.id,
            'id_instrumento': self.id_instrumento,
            'id_composicao': self.id_composicao,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create(self, id_instrumento, id_composicao):
        instrumentaco = self(id_instrumento=id_instrumento, id_composicao=id_composicao)
        db.session.add(instrumentaco)
        db.session.commit()
        return instrumentaco

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
    def get_by_id(self, id_instrumentacao):
        return self.query.get(id_instrumentacao)

    @classmethod
    def get_by_id_instrumento_and_id_composicao(cls, id_instrumento, id_composicao):
        return (cls
                .query
                .filter_by(
            id_instrumento=id_instrumento,
            id_composicao=id_composicao)
                .all())

    @classmethod
    def get_all_instrumentos_by_composicao(self, id_composicao):
        return (self
                .query
                .filter_by(id_composicao=id_composicao)
                .all())
