from dataclasses import dataclass, field

@dataclass
class Produk:
    id: str
    nama: str
    deskripsi: str
    harga: int
    kode_barang: str
    

@dataclass
class Kategori:
    id: str
    nama: str
    deskripsi: str = field(default_factory=None)