from duckdb import DuckDBPyConnection as Connection

class db_manager:
    def __init__(self, conn:Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    # SQLite 데이터베이스 초기화
    def init_db(self):
        self.cursor.execute('DROP TABLE users;') # users 테이블 자체를 삭제
        self.cursor.execute('''
            CREATE TABLE users (
                "id" TEXT PRIMARY KEY,
                "password" TEXT,
                "nickname" TEXT,
                "bookmark" TEXT
            );
        ''')
        self.conn.commit()

    def get_user_info(self, user_id:str) -> list[str]:
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone() # type: ignore
        
    def get_password_hash(self, user_id:str) -> bytes:
        self.cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
        pw_hash = self.cursor.fetchone()
        return pw_hash[0] if pw_hash else None # type: ignore

    def signup(self, user_id:str, password:bytes, nickname:str) -> bool:
        print(password)
        try:
            self.cursor.execute("INSERT INTO users (id, password, nickname) VALUES (?, ?, ?)", (user_id, password, nickname))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_acc(self, user_id:str):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def add_bookmark(self, user_id: str, webtoon_id: int):
        user_info = self.get_user_info(user_id)
        bookmark:str = user_info[3] if user_info else [] # type: ignore
        
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
        bookmark:str = user_info[3] if user_info else [] # type: ignore
        
        if bookmark:
            bookmark_list = bookmark.split(',')
            if str(webtoon_id) in bookmark_list:
                bookmark_list.remove(str(webtoon_id))
                bookmark_str = ','.join(bookmark_list)
                self.cursor.execute("UPDATE users SET bookmark = ? WHERE id = ?", (bookmark_str, user_id))
                self.conn.commit()
                return True
        return False
    