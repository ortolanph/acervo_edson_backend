from datetime import datetime

from infra import db


# quem/quando/onde/vínculo digital/etc
# 26 de Maio de 2002
# “Alguém move o ar na quietude da noite” para quinteto de sopros de madeira
# Intérpretes: Odette Ernest Dias (flauta), Jorge Postel (oboé), José Botelho (clarinete), Zdenek Svab (trompa) e Noel Devos (fagote)
# 4o Encontro de Compositores e Intérpretes Latino-Americanos
# Local: Fundação de Educação Artística
# Cidade: Belo Horizonte (MG)

# id *
# id composicao *
# Localidade (Cidade / Estado / País) String *
# Local: Teatro / Espaço cultural / Fundação / etc... String *
# Evento: Nome do evento String *
# Data Evento: data do evento *
# Estreia: True/False (só pode haver uma estreia) Boolean *
# URL do evento String
# Documento do evento string binário (arquivo do documento)

class Apresentacao(db.Model):
    """ Apresentacao entity """
    __tablename__ = 'apresentacao'

    id = db.Column(db.Integer, primary_key=True)
    id_composicao = db.Column(db.Integer, nullable=False)
    localidade = db.Column(db.String(255), nullable=False)
    local = db.Column(db.String(255), nullable=False)
    evento = db.Column(db.String(255), nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    estreia = db.Column(db.Boolean, nullable=False, default=False)
    url_evento = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (f'<Apresentacao:: '
                f'id:{self.id}, '
                f'id_composicao:{self.id_composicao}, '
                f'localidade:{self.localidade}, '
                f'local:{self.local}, '
                f'evento:{self.evento}, '
                f'data_evento:{self.data_evento.isoformat()}, '
                f'estreia:{self.estreia}, '
                f'url_evento:{self.url_evento}, '
                f'created_at: {self.created_at.isoformat() if self.created_at else None} ',
                f'updated_at: {self.updated_at.isoformat() if self.updated_at else None}>')

    def to_dict(self):
        return {
            'id': self.id,
            'id_composicao': self.id_composicao,
            'localidade': self.localidade,
            'local': self.local,
            'evento': self.evento,
            'data_evento': self.data_evento.isoformat(),
            'is_estreia': self.estreia,
            'url_evento': self.url_evento,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create(self, id_composicao, localidade, local, evento, data_evento, is_estreia, url_evento=None):
        apresentacao = self(id_composicao=id_composicao,
                            localidade=localidade,
                            local=local,
                            evento=evento,
                            data_evento=data_evento,
                            estreia=is_estreia,
                            url_evento=url_evento)

        db.session.add(apresentacao)
        db.session.commit()
        return apresentacao

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
    def get_by_id_composicao(self, id_composicao):
        return (self
                .query
                .filter_by(id_composicao=id_composicao)
                .all())

    @classmethod
    def get_unique(self, evento):
        return (self
                .query
                .filter_by(evento=evento)
                .first())
