from rich.table import Table
from rich.console import Console

console = Console()

table = Table()
table.add_column()
table.add_row(":chess_pawn:", style="purple")

console.print(table)