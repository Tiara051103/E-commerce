from pathlib import Path
import sqlite3

current_dir = Path(__file__).parent
db_path = current_dir / "mydb.db"

def get_connection():
    koneksi = sqlite3.connect(db_path)
    koneksi.row_factory = sqlite3.Row
    return koneksi
