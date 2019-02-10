"""
This is the entrypoint for the app when executed with `python -m mullemeck`.
When called, all arguments provided are passed to the `main` function in the
__init__ module.
"""

from mullemeck import main


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
