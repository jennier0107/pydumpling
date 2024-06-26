import sys
from traceback import print_exception, print_tb

from .pydumpling import save_dumping


def print_traceback_and_except(dumpling_result):
    exc_tb = dumpling_result["traceback"]
    except_extra = dumpling_result.get("exc_extra")
    exc_type = except_extra["exc_type"] if except_extra else None
    exc_value = except_extra["exc_value"] if except_extra else None
    if exc_type and exc_value:
        print_exception(exc_type, exc_value, exc_tb)
    else:
        print_tb(exc_tb)


def catch_any_exception():
    original_hook = sys.excepthook

    def _hook(exc_type, exc_value, exc_tb):
        save_dumping(exc_info=(exc_type, exc_value, exc_tb))
        original_hook(exc_type, exc_value, exc_tb)  # call sys original hook

    sys.excepthook = _hook
