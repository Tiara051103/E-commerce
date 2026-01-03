from dataclasses import dataclass
from typing import List


@dataclass
class CartItem:
    id: str
    id_cart: str
    id_produk: str
    nama_produk: str
    harga_satuan: int
    jumlah: int


@dataclass
class Cart:
    id: str
    id_user: str
    
    
