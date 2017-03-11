#!/usr/bin/python
"""The main entry point. Invoke as 'dwnldr' or 'python -m dwnldr'.
"""
import sys


def main():
    """Main function
    """
    try:
        from .cli import run
        sys.exit(run())
    except KeyboardInterrupt:
        from . import ExitStatus
        sys.exit(ExitStatus.ERROR_CTRL_C)


if __name__ == '__main__':
    main()
