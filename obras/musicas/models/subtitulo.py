from datetime import datetime

from infra import db


class Subtitulo(db.Model):
    """ Composicao entity """
    __tablename__ = 'subtitulo'

    id = db.Column(db.Integer, primary_key=True)
    id_composicao = db.Column(db.Integer)
    subtitulo = db.Column(db.String(255), nullable=False)
    lingua = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (f'<Subtitulo:: '
                f'id:{self.id}, '
                f'id_composicao:{self.id_composicao}, '
                f'subtitulo:{self.subtitulo}, '
                f'lingua:{self.lingua} '
                f'created_at: {self.created_at.isoformat() if self.created_at else None} ',
                f'updated_at: {self.updated_at.isoformat() if self.updated_at else None}>')

    def to_dict(self):
        return {
            'id': self.id,
            'id_composicao': self.id_composicao,
            'subtitulo': self.subtitulo,
            'lingua': self.lingua,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create(self, id_composicao, subtitulo, lingua):
        subtitulo = self(id_composicao=id_composicao,
                         subtitulo=subtitulo,
                         lingua=lingua)
        db.session.add(subtitulo)
        db.session.commit()
        return subtitulo

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
    def get_by_id(self, id_subtitulo):
        return self.query.get(id_subtitulo)

    @classmethod
    def get_by_composicao_id(self, id_composicao):
        return (self
                .query
                .filter_by(id_composicao=id_composicao)
                .all())

    @classmethod
    def get_by_subtitulo(self, subtitulo):
        return (self
                .query
                .filter_by(
            subtitulo=subtitulo)
                .first())
