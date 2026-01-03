from katalog.domain.entities import Produk

def produk_to_dict(produk: Produk) -> dict:
    return {
        "id": produk.id,
        "nama": produk.nama,
        "deskripsi": produk.deskripsi,
        "harga": produk.harga,
        "kode_barang": produk.kode_barang,
        "gambar": produk.gambar,
    }
    
def produk_from_dict(produk_dict: dict) -> Produk:
    return Produk(
        id=produk_dict["id"],
        nama=produk_dict["nama"],
        deskripsi=produk_dict["deskripsi"],
        harga=produk_dict["harga"],
        kode_barang=produk_dict["kode_barang"],
        gambar=produk_dict["gambar"],
    )