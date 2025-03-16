import pathlib

import click

from csviewer_tui.app import Cvit
from csviewer_tui.version import CVIT_VERSION


def check_input_file(
    ctx: click.Context, param: click.Parameter, file_path: pathlib.Path
) -> pathlib.Path:
    if file_path.suffix.lower() == ".csv":
        return file_path

    raise click.BadArgumentUsage(
        f"{file_path} is invalid file.\nYou must specify a CSV file."
    )


@click.command()
@click.version_option(CVIT_VERSION)
@click.argument(
    "file_path",
    type=click.Path(exists=True, readable=True, path_type=pathlib.Path),
    callback=check_input_file,
)
@click.option(
    "--no-header",
    is_flag=True,
    help="Do not treat the first row as a header in a CSV file.",
)
def main(file_path: pathlib.Path, no_header: bool) -> None:
    Cvit(file_path, has_header=not no_header).run()


if __name__ == "__main__":
    main()
