from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class CheckoutItem:
    id: str
    id_checkout: str
    id_produk: int
    nama_produk: str
    harga_satuan: int
    jumlah: int
    subtotal: int

@dataclass
class Checkout:
    id: str
    id_user: int
    total_harga: int
    status: str
    metode_pembayaran: str | None = None
    bank: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    items: List[CheckoutItem] | None = None