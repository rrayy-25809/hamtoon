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

    def get_user_info(self, user_id:str) -> list[str]:
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
            return True
        except IntegrityError:
            return False

    def delete_acc(self, user_id:str):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def add_bookmark(self, user_id: str, webtoon_id: int):
        user_info = self.get_user_info(user_id)
        bookmark = user_info[3] if user_info else []
        
        if bookmark:
            bookmark_list = bookmark.split(',')
            if str(webtoon_id) not in bookmark_list:
                bookmark_list.append(str(webtoon_id))
        else:
            bookmark_list = [str(webtoon_id)]
            
        bookmark_str = ','.join(bookmark_list)
        self.cursor.execute("UPDATE users SET bookmark = ? WHERE id = ?", (bookmark_str, user_id))
        self.conn.commit()
    
    def remove_bookmark(self, user_id: str, webtoon_id: int):
        user_info = self.get_user_info(user_id)
        bookmark = user_info[3] if user_info else []

        if bookmark:
            bookmark_list = bookmark.split(',')
            if str(webtoon_id) in bookmark_list:
                bookmark_list.remove(str(webtoon_id))
                bookmark_str = ','.join(bookmark_list)
                self.cursor.execute("UPDATE users SET bookmark = ? WHERE id = ?", (bookmark_str, user_id))
                self.conn.commit()
                return True
        return False
    