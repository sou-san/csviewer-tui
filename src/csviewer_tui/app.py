import csv
import pathlib

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.coordinate import Coordinate
from textual.scrollbar import ScrollBar, ScrollBarRender
from textual.widgets import Footer, Header
from textual_fastdatatable import ArrowBackend, DataTable, DataTableBackend


class MyScrollBarRender(ScrollBarRender):
    """Linux console (tty) でも文字化けしないスクロールバー"""

    HORIZONTAL_BARS = [" "]
    VERTICAL_BARS = [" "]


class FileDisplay(DataTable):
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

    # 最下部に移動したとき、行末にスクロールをしないように、 textual-fastdatatable のメソッドをオーバーライド
    def action_cursor_table_end(self, select: bool = False) -> None:
        self._set_hover_cursor(False)
        self._set_selection_anchor(select)
        self.cursor_coordinate = Coordinate(self.row_count - 1, 0)
        self._scroll_cursor_into_view(animate=True)

    # 1 ページ移動したとき、一行ずれる問題を解決するために、 textual-fastdatatable のメソッドをオーバーライド
    def action_page_up(self, select: bool = False) -> None:
        self.scroll_to(y=self.scroll_y - self.scrollable_content_region.height + 1)

    # 1 ページ移動したとき、一行ずれる問題を解決するために、 textual-fastdatatable のメソッドをオーバーライド
    def action_page_down(self, select: bool = False) -> None:
        self.scroll_to(y=self.scroll_y + self.scrollable_content_region.height - 1)


class Cvit(App[None]):
    CSS_PATH = pathlib.Path(__file__).parent / "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [Binding("q", "quit", "Quit")]

    def __init__(self, file_path: pathlib.Path, has_header: bool) -> None:
        ScrollBar.renderer = MyScrollBarRender
        self.file_path: pathlib.Path = file_path
        self.has_header: bool = has_header
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(icon="")
        yield Footer()
        yield FileDisplay(
            backend=self._create_backend(), show_cursor=False, zebra_stripes=True
        )

    def on_mount(self) -> None:
        self.title = str(self.file_path)

    def _create_backend(self) -> DataTableBackend[str]:
        with self.file_path.open(encoding="utf-8") as f:
            if self.file_path.suffix.lower() == ".csv":
                return ArrowBackend.from_records(
                    tuple(csv.reader(f)), has_header=self.has_header
                )

            return ArrowBackend.from_parquet(self.file_path)
