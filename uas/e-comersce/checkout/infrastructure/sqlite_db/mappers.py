from checkout.domain.entities import Checkout, CheckoutItem
from datetime import datetime


def checkout_to_dict(checkout: Checkout) -> dict:
    return {
        "id": checkout.id,
        "id_user": checkout.id_user,
        "total_harga": checkout.total_harga,
        "status": checkout.status,
        "created_at": checkout.created_at.isoformat(),
    }


def checkout_from_dict(row: dict) -> Checkout:
    return Checkout(
        id=row["id"],
        id_user=row["id_user"],
        total_harga=row["total_harga"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
        items=[]
    )


def checkout_item_to_dict(item: CheckoutItem) -> dict:
    return {
        "id": item.id,
        "id_checkout": item.id_checkout,
        "id_produk": item.id_produk,
        "nama_produk": item.nama_produk,
        "harga_satuan": item.harga_satuan,
        "jumlah": item.jumlah,
        "subtotal": item.subtotal,
    }


def checkout_item_from_dict(row: dict) -> CheckoutItem:
    return CheckoutItem(
        id=row["id"],
        id_checkout=row["id_checkout"],
        id_produk=row["id_produk"],
        nama_produk=row["nama_produk"],
        harga_satuan=row["harga_satuan"],
        jumlah=row["jumlah"],
        subtotal=row["subtotal"],
    )
