import typer

from pos.pos_system import PosSystem

app = typer.Typer()
pos = PosSystem()


@app.command("list")
def list_store_info():
    pos.list_store_info()


@app.command("simulate")
def simulate_pos_system():
    pos.simulate()


@app.command("report")
def generate_report():
    pos.generate_report()
