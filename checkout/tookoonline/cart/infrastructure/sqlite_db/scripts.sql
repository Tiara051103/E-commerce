CREATE TABLE cart (
    id TEXT PRIMARY KEY,
    id_user TEXT NOT NULL
);

CREATE TABLE cart_item (
    id TEXT PRIMARY KEY,
    id_cart TEXT NOT NULL,
    id_produk TEXT NOT NULL,
    nama_produk TEXT NOT NULL,
    harga_satuan REAL NOT NULL,
    jumlah INTEGER NOT NULL,
    FOREIGN KEY (id_cart) REFERENCES cart(id)
);
