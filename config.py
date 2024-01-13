"""
.env 파일로 부터 각종 데이터베이스 인증 정보와 암호화에 필요한 정보를 불러옵니다.
"""

import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIAL_SECRET_KEY = os.getenv("CREDENTIAL_SECRET_KEY", "")
CREDENTIAL_ALGORITHM = os.getenv("CREDENTIAL_ALGORITHM", "")

DB_CONFIG = {
    "rdb": os.getenv("RDB", "postgresql+asyncpg"),
    "db_user": os.getenv("DB_USER", ""),
    "db_password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "host.docker.internal"),
    "port": os.getenv("DB_PORT", "5432"),
    "db": os.getenv("DB", ""),
}
