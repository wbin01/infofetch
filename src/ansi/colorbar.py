#!/usr/bin/env python3


class ColorBar(object):
    """..."""
    def __init__(self, color: tuple | list) -> None:
        """...

        :param color: RGB tuple or list like (255, 255, 255)
        """
        self.__color = color
        self.__color_item_width = 1
        self.__is_legacy = False
        self.__is_mirrored = True
        self.__colorbar = None

    @property
    def color(self) -> tuple | list:
        """..."""
        return self.__color

    @color.setter
    def color(self, color: tuple | list) -> None:
        self.__color = color

    @property
    def color_item_width(self) -> int:
        """..."""
        return self.__color_item_width

    @color_item_width.setter
    def color_item_width(self, width: int) -> None:
        self.__color_item_width = width

    @property
    def is_legacy(self) -> bool:
        """..."""
        return self.__is_legacy

    @is_legacy.setter
    def is_legacy(self, value: bool) -> None:
        self.__is_legacy = value

    @property
    def is_mirrored(self) -> bool:
        """..."""
        return self.__is_mirrored

    @is_mirrored.setter
    def is_mirrored(self, value: bool) -> None:
        self.__is_mirrored = value

    @property
    def colorbar(self) -> str:
        if self.__colorbar:
            return self.__colorbar

        self.__update_colorbar()
        return self.__colorbar

    @colorbar.setter
    def colorbar(self, colorbar: str) -> None:
        self.__colorbar = colorbar

    @staticmethod
    def __get_legacy_colorbar() -> str:
        # ...
        return (
            '\x1b[48;2;53;53;159m \x1b[48;2;64;113;191m '
            '\x1b[48;2;64;170;191m \x1b[48;2;127;212;169m '
            '\x1b[48;2;169;212;127m \x1b[48;2;191;191;64m '
            '\x1b[48;2;191;170;64m \x1b[48;2;191;148;64m '
            '\x1b[48;2;191;106;64m \x1b[48;2;196;57;57m '
            '\x1b[48;2;148;50;50m \x1b[48;2;138;50;116m '
            '\x1b[48;2;107;61;166m \x1B[0m')

    def __update_colorbar(self) -> None:
        # ...
        if self.__is_legacy:
            self.__colorbar = self.__get_legacy_colorbar()
            return

        self.__darken_color(50)
        colors_sig = []
        for num in self.__color:
            color_sig = num + '+' if int(num) + 100 < 255 else num + '-'
            colors_sig.append(color_sig)

        colors = []
        for _ in range(10):
            update_colors_sig = []
            ansi = ''

            for num, color in enumerate(colors_sig):
                if color[-1] == '+':
                    new_color = int(color[:-1]) + 10
                    update_colors_sig.append(str(new_color) + '+')
                else:
                    new_color = int(color[:-1]) - 10
                    update_colors_sig.append(str(new_color) + '-')

                if num == 0:
                    ansi += '\x1b[48;2;' + str(new_color)
                elif num == 1:
                    ansi += ';' + str(new_color)
                else:
                    ansi += ';' + str(new_color) + 'm'
                    ansi += ' ' * self.__color_item_width

            colors_sig = update_colors_sig
            colors.append(ansi)

        if self.__is_mirrored:
            colors.reverse()
            colors_rev = colors.copy()
            del colors_rev[0]
            colors.reverse()

            colorbar = ''.join([str(x) for x in colors + colors_rev])
        else:
            colorbar = ''.join([str(x) for x in colors])

        self.__colorbar = colorbar + '\x1B[0m'

    def __darken_color(self, weight: int) -> None:
        # ...
        colors = []
        for num in self.__color:
            int_num = int(num)
            if int_num - weight >= 0:
                colors.append(str(int_num - weight))
            else:
                colors.append(num)
        self.__color = colors
