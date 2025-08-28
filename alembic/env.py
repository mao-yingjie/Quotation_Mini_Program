"""配置 Alembic 迁移环境的脚本"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from contractor.db import DATABASE_URL, engine
from contractor.models import SQLModel

# Alembic 配置对象，可访问 .ini 文件中的值
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 解析配置文件以配置 Python 日志
# 该行用于初始化日志器
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 在此处添加模型的 MetaData 对象
# 以支持自动生成迁移
# 例如: from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """在离线模式下运行迁移"""
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在在线模式下运行迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
