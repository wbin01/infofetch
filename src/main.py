#!/usr/bin/env python3
import systeminfo


def main() -> None:
    """..."""
    info = systeminfo.SystemInfo()
    info.fetch()


if __name__ == '__main__':
    main()
