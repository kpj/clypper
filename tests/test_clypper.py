#!/usr/bin/env python

"""Tests for `clypper` package."""

import os
import shutil

import pytest

from click.testing import CliRunner

from clypper import clypper
from clypper import cli


def test_command_line_interface(tmp_path):
    """Test the CLI."""
    runner = CliRunner()

    outfile = tmp_path / 'output.mp4'
    clyp_tmp = tmp_path / 'temp'

    os.chdir('tests')
    result = runner.invoke(
        cli.main, [
            '-i', 'test_input.txt',
            '-o', outfile,
            '--tmp-dir', clyp_tmp
        ],
        catch_exceptions=False)
    shutil.rmtree(clyp_tmp)

    assert result.exit_code == 0
    assert os.path.exists(outfile)
