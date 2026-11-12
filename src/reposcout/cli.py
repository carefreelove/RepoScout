"""RepoScout command line entry points."""

import json
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console

from reposcout.agent import execute
from reposcout.domain import ResearchError
from reposcout.reporting import export
from reposcout.settings import Settings
from reposcout.storage import Store

app = typer.Typer(help="RepoScout｜开源项目调研 Agent", no_args_is_help=True, pretty_exceptions_enable=False)
console = Console()


def progress(stage: str):
    console.print(stage, style="dim", markup=False)


@app.callback()
def configure():
    load_dotenv()


def finish(store: Store, run_id: str, path: Path):
    status = store.run(run_id)["status"]
    console.print(f"任务 {run_id} · {status}")
    console.print(str(path.resolve() / "report.md"))
    if status != "completed":
        for error in store.events(run_id)[-3:]:
            console.print(f"{error['code']} — {error['detail']}")
        raise typer.Exit(130 if status == "cancelled" else 1)


@app.command()
def research(request: str = typer.Argument(..., min=1),
             search_limit: int = typer.Option(10, min=1, max=30),
             analyze_limit: int = typer.Option(3, min=1, max=10)):
    """从自然语言需求开始一次公开 GitHub 调研。"""
    if not request.strip():
        raise typer.BadParameter("调研需求不能为空")
    settings = Settings(search_limit=search_limit, analyze_limit=analyze_limit)
    store = Store(settings, on_event=progress)
    run_id = store.create(request)
    console.print(f"开始任务 {run_id}")
    finish(store, run_id, execute(store, run_id))


@app.command()
def show(run_id: str):
    """导出已保存的任务状态与报告。"""
    try:
        store = Store(Settings())
        with store.lock(run_id):
            path = export(store, run_id)
        console.print((path / "report.md").read_text(), markup=False)
    except ResearchError as exc:
        console.print(str(exc))
        raise typer.Exit(1) from exc


@app.command()
def resume(run_id: str):
    """恢复同一任务，沿用原请求、证据、调用限额与费用账本。"""
    try:
        initial = Store(Settings())
        config = json.loads(initial.run(run_id)["config"])
        config["home"] = initial.settings.home
        store = Store(Settings.model_validate(config), on_event=progress)
        finish(store, run_id, execute(store, run_id, resume=True))
    except ResearchError as exc:
        console.print(str(exc))
        raise typer.Exit(1) from exc


@app.command()
def acknowledge_usage(ticket: str):
    """人工接受某次未知用量的最高预留额，保留费用并解除该记录的调用冻结。"""
    try:
        cost = Store(Settings()).acknowledge_uncertain(ticket)
        console.print(f"已保留最高预留 {cost / 1e6:.6f} 元，实际用量仍未确认")
    except ResearchError as exc:
        console.print(str(exc))
        raise typer.Exit(1) from exc


@app.command()
def evaluate(suite: str = "smoke", live: bool = False):
    """运行固定问题集。默认合成离线回放，--live 会产生模型费用。"""
    if suite == "evidence":
        from reposcout.evidence_evaluation import evaluate_evidence
        path = evaluate_evidence(Store(Settings()), live=live)
        console.print(str(path.resolve()))
        result = json.loads(path.read_text())
        if not result["passed"]:
            raise typer.Exit(1)
        return
    if suite != "smoke":
        raise typer.BadParameter("支持 --suite smoke 或 --suite evidence")
    from reposcout.evaluation import evaluate as run_evaluation
    path = run_evaluation(Store(Settings()), live=live)
    console.print(str(path.resolve()))
    data = json.loads(path.read_text())
    if any(not r["checks"]["valid_report"] for r in data["results"]):
        raise typer.Exit(1)
