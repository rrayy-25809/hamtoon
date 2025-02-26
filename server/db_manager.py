from sqlite3 import Connection, IntegrityError, Cursor

class db_manager:
    conn:Connection = None
    cursor:Cursor = None

    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    # SQLite 데이터베이스 초기화
    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                "id" TEXT PRIMARY KEY,
                "password" TEXT,
                "nickname" TEXT,
                "bookmark" TEXT
            );
        ''')
        self.conn.commit()

    def get_user_info(self, user_id:str):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result
        
    def login(self, user_id:str, password:str) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE id = ? AND password = ?", (user_id, password))
        return self.cursor.fetchone()

    def signup(self, user_id:str, password:str, nickname:str) -> bool:
        try:
            self.cursor.execute("INSERT INTO users (id, password, nickname) VALUES (?, ?, ?)", (user_id, password, nickname))
            self.conn.commit()
            self.cursor.close()
            return True
        except IntegrityError:
            return False

    def delete_acc(self, user_id:str):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        self.conn.close()