#!/usr/bin/env python3
import os
import subprocess

import ansicolorimage
import systeminfo
import formattedsysteminfo


class SystemInfo(object):
    """..."""

    def __init__(self) -> None:
        """..."""
        self.__height = 25
        self.__width = 50
        self.__colorbar_size = 1
        self.__legacy_colorbar = False
        self.__mirrored_colorbar = True
        self.__base_dir = os.path.dirname(os.path.abspath(__file__))
        self.__os_logo = self.__get_system_logo()
        self.__os_informations = self.__get_system_info()

    def fetch(self) -> None:
        """..."""
        self.__set_same_amount_of_lines_for_logo_and_info()
        for img_line, text_line in zip(
                self.__os_logo.ansi_lines, self.__os_informations):
            print(img_line, text_line)

    def __get_system_logo(self) -> ansicolorimage:
        # ...
        sysinfo = systeminfo.SystemInfo()
        img = os.path.join('/usr/share/pixmaps', f'{sysinfo.name_id}.png')
        if not os.path.isfile(img):
            img = os.path.join(self.__base_dir, 'resources', 'linux.png')

        return ansicolorimage.AnsiColorImage(
            url_image=img, contrast=1.3, brightness=0.85)

    def __get_system_info(self) -> list:
        # ...
        info = ''

        _cmd = subprocess.Popen(
            ['tput', 'cols'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tput_cols, _stderr = _cmd.communicate()

        system_info_items = formattedsysteminfo.FormattedSystemInfo()

        for key, value in system_info_items.system_fetch_as_dict.items():
            value_width = int(tput_cols) - len(key) - self.__os_logo.width - 3

            if len(value) > value_width:
                info += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__os_logo.image_accent_color,
                    key,
                    value[:value_width - 3] + '...')
            else:
                info += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__os_logo.image_accent_color, key, value)

        return info.split('\n')

    def __create_color_bar(self) -> str:
        # ...
        if self.__legacy_colorbar:
            return (
                '\x1b[48;2;53;53;159m \x1b[48;2;64;113;191m '
                '\x1b[48;2;64;170;191m \x1b[48;2;127;212;169m '
                '\x1b[48;2;169;212;127m \x1b[48;2;191;191;64m '
                '\x1b[48;2;191;170;64m \x1b[48;2;191;148;64m '
                '\x1b[48;2;191;106;64m \x1b[48;2;196;57;57m '
                '\x1b[48;2;148;50;50m \x1b[48;2;138;50;116m '
                '\x1b[48;2;107;61;166m \x1B[0m')

        colors_sig = []
        for x in self.__os_logo.image_accent_color.split(';'):
            color_sig = x + '+' if int(x) + 100 < 255 else x + '-'
            colors_sig.append(color_sig)

        colors = []
        for x in range(10):
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
                    ansi += ' ' * self.__colorbar_size

            colors_sig = update_colors_sig
            colors.append(ansi)

        if self.__mirrored_colorbar:
            colors.reverse()
            colors_rev = colors.copy()
            del colors_rev[0]
            colors.reverse()
            return ''.join([str(x) for x in colors + colors_rev]) + '\x1B[0m'

        return ''.join([str(x) for x in colors]) + '\x1B[0m'

    def __set_same_amount_of_lines_for_logo_and_info(self) -> None:
        # Same height

        len_image = len(self.__os_logo.ansi_lines)
        len_info = len(self.__os_informations)

        color_bar = self.__create_color_bar()

        if len_image < len_info:
            self.__os_informations[-1] = color_bar

            for _ in range(len_info - len_image):
                self.__os_logo.ansi_lines.append(' ' * self.__os_logo.width)

        else:
            for _ in range(len_image - len_info):
                self.__os_informations.append(' ')

            self.__os_informations[-1] = color_bar


def main() -> None:
    """..."""
    info = SystemInfo()
    info.fetch()


if __name__ == '__main__':
    main()
