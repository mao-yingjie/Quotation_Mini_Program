"""CLI 命令测试文件，验证应用的命令行接口。"""

from typer.testing import CliRunner
from contractor.cli import app


def test_template_list_outputs_known_template():
    """模板列表命令应输出已知模板名"""
    # 创建 Typer 的 CLI 运行器
    runner = CliRunner()
    # 调用 template-list 命令并获取输出
    result = runner.invoke(app, ["template-list"])
    # 验证命令执行成功并包含指定模板
    assert result.exit_code == 0
    assert "basic_en" in result.stdout
