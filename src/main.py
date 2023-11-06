#!/usr/bin/env python3
import logging
import sys

import infofetch


class Application(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__args_k_v = {}
        self.__errors_found = False
        self.__app = infofetch.InfoFetch()

    def __create_args(self) -> None:
        # ...
        for arg in ' '.join(sys.argv[1:]).split(' -'):
            arg = arg.strip().strip('"').strip("'")

            if ' ' in arg:
                key, value = arg.split(' ')
                self.__args_k_v[key] = value.strip('"').strip("'")
            else:
                self.__args_k_v[arg] = None

    def __set_args(self) -> None:
        # ...
        if len(sys.argv) < 1:
            return

        self.__create_args()
        for key, value in self.__args_k_v.items():
            if key == '--colobar-item-width':
                self.__arg_colobar_item_width(value)
            elif key == '--colorbar-legacy':
                self.__arg_colorbar_legacy(value)
            elif key == '--colorbar-small':
                self.__arg_colorbar_small(value)
            elif key == '--help' or key == '-h':
                self.__arg_help(value)
            else:
                print(f"Argument '{key}' unknown. Use --help.")
                sys.exit(1)

            if self.__errors_found:
                sys.exit(1)

    def __arg_colobar_item_width(self, value) -> None:
        # ...
        if value.isdigit():
            self.__app.colobar_item_width = int(value)
        elif value == 'auto':
            self.__app.colobar_item_width = 1
        else:
            self.__errors_found = True
            print(f"Error '{value}'.\nThe value must be an integer such as "
                  "'1' or '2', or 'auto' for the default value.")

    def __arg_colorbar_legacy(self, value) -> None:
        # ...
        if value == 'true':
            self.__app.colorbar_is_legacy = True
        elif value == 'false' or value == 'auto':
            self.__app.colorbar_is_legacy = False
        else:
            self.__errors_found = True
            print(f"Error '{value}'.\nThe value needs to be 'true', 'false' or"
                  " 'auto' for the default value.")

    def __arg_colorbar_small(self, value) -> None:
        # ...
        if value == 'true':
            self.__app.colorbar_is_mirrored = False
        elif value == 'false' or value == 'auto':
            self.__app.colorbar_is_mirrored = True
        else:
            self.__errors_found = True
            print(f"Error '{value}'.\nThe value needs to be 'true', 'false' or"
                  " 'auto' for the default value.")

    @staticmethod
    def __arg_help(value) -> None:
        # ...
        if value:
            print(f"Argument '{value}' unknown. Use --help.")
            sys.exit(1)

        print(
            'infofetch <--arg> <value>\n'
            'infofetch <--arg>\n\n'
            '--help, -h                Display this help and exit\n'
            '--colobar-item-width <1>  Chars num each color uses\n'
            '--colorbar-legacy <true>  Use the old color bar\n'
            '--colorbar-small <false>  Only half of the color bar\n')
        sys.exit(0)

    def main(self) -> None:
        """..."""
        self.__set_args()
        self.__app.fetch()


if __name__ == '__main__':
    app = Application()
    sys.exit(app.main())
