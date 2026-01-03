from pathlib import Path
import sqlite3

# folder sqlite_db
current_dir = Path(__file__).parent

# PATH database
DB_PATH = current_dir / "cart.db"


def get_connection():
    conn = sqlite3.connect(
        db_path,
        timeout=30,              # ⬅ tunggu sampai 30 detik
        check_same_thread=False  # ⬅ wajib untuk Flask
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

