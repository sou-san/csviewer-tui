import pathlib

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class Cvit(App[None]):
    ENABLE_COMMAND_PALETTE = False

    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path: pathlib.Path = file_path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = str(self.file_path)
