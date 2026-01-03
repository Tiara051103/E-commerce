from pathlib import Path
import sqlite3

current_dir = Path(__file__).parent
db_path = current_dir / "katalog.db"

def get_connection():
    conn = sqlite3.connect(
        db_path,
        timeout=30,              # ⬅ tunggu sampai 30 detik
        check_same_thread=False  # ⬅ wajib untuk Flask
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
def init_db():
    conn = get_connection()
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.close()
