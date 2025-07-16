from infra.database import db


class InstrumentoMusical(db.Model):
    __tablename__ = 'instrumento_musical'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    grupo = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'grupo': self.grupo
        }

    def __repr__(self):
        return f'<InstrumentoMusical {self.id}, {self.nome}, {self.grupo}'
