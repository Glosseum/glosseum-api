from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig


alembic_config = AlembicConfig("alembic.ini")

alembic_config.set_main_option("sqlalchemy.url", "sqlite+aiosqlite:///test.db")
alembic_upgrade(alembic_config, "head")
