from pydantic import BaseModel, field_validator
from typing import Optional

class FilterProdukDTO(BaseModel):
    nama: Optional[str] = None
    kategori_id: Optional[int] = None
    brand_id: Optional[int] = None
    warna: Optional[str] = None
    ukuran: Optional[str] = None
    stok_min: Optional[int] = None
    harga_min: Optional[int] = None
    harga_max: Optional[int] = None

    # =========================
    # UBAH STRING KOSONG → None
    # =========================
    @field_validator(
        "nama",
        "brand_id",
        "warna",
        "ukuran",
        mode="before"
    )
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v.strip()

    # =========================
    # KONVERSI KE INT
    # =========================
    @field_validator(
        "kategori_id",
        "stok_min",
        "harga_min",
        "harga_max",
        mode="before"
    )
    @classmethod
    def str_to_int(cls, v):
        if v in ("", None):
            return None
        return int(v)

    class Config:
        from_attributes = True
