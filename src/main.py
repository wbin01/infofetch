#!/usr/bin/env python3
import sys

import infofetch


class Application(object):
    """..."""
    def __init__(self, args: list) -> None:
        """..."""
        self.__args = args
        self.__app = infofetch.InfoFetch()

    def __set_args(self) -> None:
        # ...
        if not len(self.__args) > 1:
            return

        for key, value in {
            x.split('=')[0]: x.split('=')[1].strip('"').strip("'")
                for x in self.__args if '=' in x}.items():

            if key == '--colobar-item-width':
                if value.isdigit():
                    self.__app.colobar_item_width = int(value)
                elif value == 'auto':
                    self.__app.colobar_item_width = 1
                else:
                    raise ValueError(
                        "The value must be an integer ('1' or '2'), "
                        "or the default value ('auto').")

            elif key == '--colorbar-legacy':
                if value == 'true':
                    self.__app.colorbar_is_legacy = True
                elif value == 'false' or value == 'auto':
                    self.__app.colorbar_is_legacy = False
                else:
                    raise ValueError(
                        "The value needs to be 'true', 'false' or 'auto' "
                        "for the default value.")

            elif key == '--colorbar-small':
                pass

            elif key == '--colo':
                pass

            elif key == '--col':
                pass

            elif key == '--co':
                pass

            elif key == '--colo':
                pass

    def main(self) -> None:
        """..."""
        self.__set_args()
        self.__app.fetch()


if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.main())
