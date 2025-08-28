.PHONY: install init-db

# ---------------------------------------
# Makefile 用于封装项目常用命令
# ---------------------------------------

# 安装运行和开发依赖
install:
	poetry install -E runtime -E dev

# 初始化应用数据库
init-db:
	poetry run contractor init-db
