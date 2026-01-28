from dataclasses import dataclass, field

@dataclass
class Produk:
    nama: str
    deskripsi: str
    harga: int
    kode_barang: str
    brand_id: int | None = None
    gambar: str | None = None
    id: int | None = None
    
@dataclass
class Kategori:
    nama: str
    id: int | None = None
    deskripsi: str | None = None

@dataclass
class Brand:
    nama: str = ""
    id: int | None = None

@dataclass
class VarianProduk:
    produk_id: int = 0
    warna: str | None = None
    ukuran: str | None = None
    stok: int = 0
    id: int | None = None