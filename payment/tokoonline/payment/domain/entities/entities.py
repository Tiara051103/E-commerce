from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Payment:
    id: str
    id_checkout: str
    id_user: int
    metode: str
    total_harga: int
    status: str      
    created_at: datetime = datetime.now()
    paid_at: Optional[datetime] = None
