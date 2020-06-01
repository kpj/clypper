"""Console script for clypper."""
import sys
from pathlib import Path

import click

from .clypper import handle


@click.command()
@click.option(
    '-i', '--input', 'input_file',
    required=True, type=click.Path(exists=True, dir_okay=False))
@click.option(
    '-o', '--output', 'output_file',
    required=True, type=click.Path(dir_okay=False))
@click.option(
    '--tmp-dir', 'temp_dir',
    default='tmp_clypper', type=click.Path())
def main(input_file, output_file, temp_dir):
    """Console script for clypper."""
    handle(input_file, output_file, Path(temp_dir))
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
