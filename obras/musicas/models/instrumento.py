from datetime import datetime

from infra import db


class Instrumento(db.Model):
    """ Instrumento entity """
    __tablename__ = 'instrumento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (f'<Instrumento:: '
                f'id:{self.id}, '
                f'nome:{self.nome}, '
                f'grupo:{self.grupo} '
                f'created_at: {self.created_at.isoformat() if self.created_at else None} ',
                f'updated_at: {self.updated_at.isoformat() if self.updated_at else None}>')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'grupo': self.grupo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create(self, nome, grupo):

        instrumento = self(nome=nome, grupo=grupo)
        db.session.add(instrumento)
        db.session.commit()
        return instrumento

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
    def get_by_id(self, id_instrumento):
        return self.query.get(id_instrumento)

    @classmethod
    def get_all(self):
        return self.query.all()

    @classmethod
    def get_by_nome(self, nome):
        return (self
                .query
                .filter_by(
            nome=nome)
                .first())

    @classmethod
    def get_by_grupo(self, grupo):
        return (self
                .query
                .filter_by(
            grupo=grupo)
                .all())
