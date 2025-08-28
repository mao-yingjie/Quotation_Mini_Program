---
title: 系统架构
---

<!-- 文件作用：概述项目的系统架构和核心组件 -->

# 系统架构

本项目采用模块化设计，核心组件如下：

1. **CLI 层**：基于 [Typer](https://typer.tiangolo.com/) 构建的命令行工具，
   提供数据库初始化、合同创建、渲染及报表等命令。
2. **服务层**：位于 `src/contractor/services`，负责模板渲染、PDF/Word
   转换、报表统计和 Git 版本管理等具体逻辑。
3. **数据层**：使用 [SQLModel](https://sqlmodel.tiangolo.com/) 定义的
   数据模型与 SQLite 数据库交互。
4. **模板与资源**：`templates/` 目录包含基于 Jinja2 的 LaTeX 模板，
   `contracts/` 用于存放渲染后的合同文件。

整体流程如下：

1. 用户通过 CLI 输入命令。
2. CLI 调用服务层进行业务处理。
3. 数据层负责读写数据库，模板层完成合同渲染并输出到指定目录。

