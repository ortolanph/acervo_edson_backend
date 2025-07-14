from datetime import datetime
from uuid import UUID


class Observacao:
    id: UUID
    id_obra_musical: UUID
    registrada_em: datetime
    observacao: str
