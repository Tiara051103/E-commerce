from cart.domain.entities import Cart, CartItem
from cart.dto.cart_dto import CartDTO, CartItemDTO

def cart_item_to_dto(item: CartItem) -> CartItemDTO:
    return CartItemDTO(
        id=item.id,
        id_produk=item.id_produk,
        nama_produk=item.nama_produk,
        harga_satuan=item.harga_satuan,
        jumlah=item.jumlah,
        total_harga=item.harga_satuan * item.jumlah,
    )
def cart_item_from_dto(
    dto: CartItemDTO,
    id_keranjang: str,
) -> CartItem:
    return CartItem(
        id=dto.id,
        id_keranjang=id_keranjang,
        id_produk=dto.id_produk,
        nama_produk=dto.nama_produk,
        harga_satuan=dto.harga_satuan,
        jumlah=dto.jumlah,
    )

def cart_to_dto(cart: Cart, items: list[CartItem]) -> CartDTO:
    item_dtos = [cart_item_to_dto(item) for item in items]

    total_cart = sum(item.total_harga for item in item_dtos)

    return CartDTO(
        id=cart.id,
        id_user=cart.id_user,
        items=item_dtos,
        total_cart=total_cart,
    )

