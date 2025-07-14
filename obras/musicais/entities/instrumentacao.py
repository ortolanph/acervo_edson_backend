from uuid import UUID

from obras.musicais.entities.instrumento_musical import InstrumentoMusical


class Instrumentacao:
    id: UUID
    id_obra_musical: UUID
    instrumento: InstrumentoMusical
    interprete: str
