from infra.database import db


class ComposicaoMusical(db.Model):
    __tablename__ = 'composicao_musical'

    id = db.Column(db.Integer, primary_key=True)
    numero_composicao = db.Column(db.String(80), unique=True, nullable=False)
    titulo = db.Column(db.String(255), unique=True, nullable=False)
    data_composicao = db.Column(db.Date(), nullable=False)
    categoria = db.Column(db.String(255), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'numero_composicao': self.numero_composicao,
            'titulo': self.titulo,
            'data_composicao': self.data_composicao,
            'categoria': self.categoria
        }

    def __repr__(self):
        return f'<ComposicaoMusical {self.id}, {self.numero_composicao}, {self.titulo}, {self.data_composicao}, {self.categoria}>'
