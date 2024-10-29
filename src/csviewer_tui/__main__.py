import pathlib

import click

from csviewer_tui.app import Cvit


def is_csv_file(
    ctx: click.Context, param: click.Parameter, file_path: pathlib.Path
) -> pathlib.Path:
    if file_path.suffix.lower() == ".csv":
        return file_path

    raise click.BadArgumentUsage(
        f"{file_path} is invalid file.\nYou must specify a CSV file."
    )


@click.command()
@click.argument(
    "file_path",
    type=click.Path(exists=True, readable=True, path_type=pathlib.Path),
    callback=is_csv_file,
)
def main(file_path: pathlib.Path) -> None:
    Cvit(file_path).run()


if __name__ == "__main__":
    main()
