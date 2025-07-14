from datetime import datetime
from uuid import UUID

from obras.musicais.entities.categoria import Categoria
from obras.musicais.entities.estreia import Estreia
from obras.musicais.entities.instrumentacao import Instrumentacao
from obras.musicais.entities.observacao import Observacao
from obras.musicais.entities.subtitulo import Subtitulo


class ObraMusical:
    id: UUID
    composicao: str
    data_composicao: datetime
    sub_titulos: [Subtitulo]
    categoria_principal: Categoria
    categorias: [Categoria]
    instrumentacao: [Instrumentacao]
    estreia: Estreia
    observacoes: [Observacao]
