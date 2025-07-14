from datetime import datetime
from uuid import UUID


class Estreia:
    id: UUID
    id_obra_musical: UUID
    data: datetime
    local: str
    documento: bytearray
