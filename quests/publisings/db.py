import psycopg2
from typing import Optional

# 사용자 요청에 따라 DB 연결 정보를 직접 설정
DB_HOST: Optional[str] = "db_postgresql"
DB_PORT: Optional[str] = "5432"
POSTGRES_DB: Optional[str] = "main_db"
POSTGRES_USER: Optional[str] = "admin"
POSTGRES_PASSWORD: Optional[str] = "admin123"

def get_db_connection():
    """PostgreSQL 데이터베이스 연결을 설정하고 반환합니다."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        # 연결 실패 시 None 반환
        return None