from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import gzip
import inspect
import pdb
import pickle
import types

import dill
from packaging.version import parse

from .fake_types import FakeCode, FakeFrame, FakeTraceback


def load_dumpling(filename):
    with gzip.open(filename, "rb") as f:
        try:
            return dill.load(f)
        except Exception:
            return pickle.load(f)


def mock_inspect():
    inspect.isframe = lambda obj: isinstance(
        obj, types.FrameType) or obj.__class__ == FakeFrame
    inspect.istraceback = lambda obj: isinstance(
        obj, types.TracebackType) or obj.__class__ == FakeTraceback
    inspect.iscode = lambda obj: isinstance(
        obj, types.CodeType) or obj.__class__ == FakeCode


def debug_dumpling(dump_file, pdb=pdb):
    mock_inspect()
    dumpling = load_dumpling(dump_file)
    if not parse("0.0.1") <= parse(dumpling["version"]) < parse("1.0.0"):
        raise ValueError("Unsupported dumpling version: %s" %
                         dumpling["version"])
    tb = dumpling["traceback"]
    pdb.post_mortem(tb)
