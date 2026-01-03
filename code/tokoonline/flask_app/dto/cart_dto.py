from pydantic import BaseModel
from typing import List, Optional

class TambahItemCartDTO(BaseModel):
    id_user: str
    id_produk: str
    jumlah: int = 1

    class Config:
        from_attributes = True

class UbahJumlahItemDTO(BaseModel):
    id_item: str
    jumlah: int
    id_user: str

    class Config:
        from_attributes = True

class CartItemDTO(BaseModel):
    id: str
    id_produk: str
    nama_produk: str
    harga_satuan: float
    jumlah: int
    total_harga: float

    class Config:
        from_attributes = True

class CartDTO(BaseModel):
    id: str
    id_user: str
    items: List[CartItemDTO]
    total_cart: float

    class Config:
        from_attributes = True

