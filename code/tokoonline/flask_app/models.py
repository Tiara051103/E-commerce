from pydantic import BaseModel, Field
from typing import Optional, Any

class Produk(BaseModel):
    nama: str
    deskripsi: str
    harga: int
    kode_barang: str
    brand_id: int | None = None
    gambar: str | None = None
    id: int | None = None
    
