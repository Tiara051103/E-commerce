from auth.domain.entities import User
from auth.domain.repositories import UserRepository

from ..mappers import user_to_dict, user_from_dict

from ..db_settings import get_connection

class UserRepositorySQLite(UserRepository):
    def __init__(self):
        pass
    
    def add(self, user: User) -> User:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("INSERT INTO users (id, username, password, status) VALUES (?, ?, ?, ?)", (user.id, user.username, user.password, user.status))
        koneksi.commit()
        cursor.close()
        koneksi.close()
        return user
    
    def update(self, user: User) -> User:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("UPDATE users SET username=?, password=?, status=? WHERE id=?", (user.username, user.password, user.status, user.id))
        koneksi.commit()
        cursor.close()
        koneksi.close()
        return user
    
    def delete_by_id(self, id: str) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (id,))
        koneksi.commit()
        cursor.close()
        koneksi.close()
        
    def get_all(self) -> list[User]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [user_from_dict(row) for row in rows]
    
    def get_by_id(self, id: str) -> User | None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return None if row is None else user_from_dict(row)

    def get_by_username(self, username: str) -> User | None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return None if row is None else user_from_dict(row)