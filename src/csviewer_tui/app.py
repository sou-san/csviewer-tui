import csv
import pathlib

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.scrollbar import ScrollBar, ScrollBarRender
from textual.widgets import Footer, Header
from textual_fastdatatable import ArrowBackend, DataTable, DataTableBackend


class MyScrollBarRender(ScrollBarRender):
    """Linux console (tty) でも文字化けしないスクロールバー"""

    HORIZONTAL_BARS = [" "]
    VERTICAL_BARS = [" "]


class CsvFileDisplay(DataTable):
    BINDINGS = [
        Binding("k", "cursor_up", "Scroll Up"),
        Binding("j", "cursor_down", "Scroll Down"),
        Binding("h", "cursor_left", "Scroll Left"),
        Binding("l", "cursor_right", "Scroll Right"),
        Binding("g", "cursor_table_start", "Go to Top"),
        Binding("G", "cursor_table_end", "Go to Bottom"),
        Binding("b", "page_up", "Page Up"),
        Binding("f", "page_down", "Page Down"),
    ]


class Cvit(App[None]):
    CSS_PATH = "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [Binding("q", "exit_app", "Exit")]

    def __init__(self, file_path: pathlib.Path) -> None:
        ScrollBar.renderer = MyScrollBarRender
        self.file_path: pathlib.Path = file_path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(icon="")
        yield Footer()
        yield CsvFileDisplay(
            backend=self._create_backend(), show_cursor=False, zebra_stripes=True
        )

    def on_mount(self) -> None:
        self.title = str(self.file_path)

    def _create_backend(self) -> DataTableBackend[str]:
        with self.file_path.open(encoding="utf-8") as f:
            return ArrowBackend.from_records(tuple(csv.reader(f)), has_header=True)

    def action_exit_app(self) -> None:
        self.exit()
