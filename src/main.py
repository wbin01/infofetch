#!/usr/bin/env python3
import os
import subprocess

import ansicolorimage
import systeminfo
import formattedsysteminfo
import colorbar


class SystemInfo(object):
    """..."""

    def __init__(self) -> None:
        """..."""
        self.__base_dir = os.path.dirname(os.path.abspath(__file__))

        self.__logo_height = 25
        self.__logo_width = 50
        self.__logo = self.__get_logo()

        self.__infos = self.__get_infos()

        self.__colorbar_item_width = 1
        self.__colorbar_is_legacy = False
        self.__colorbar_is_mirrored = True

    def fetch(self) -> None:
        """..."""
        self.__set_same_amount_of_lines_for_logo_and_info()
        for img_line, text_line in zip(
                self.__logo.ansi_lines, self.__infos):
            print(img_line, text_line)

    def __get_logo(self) -> ansicolorimage:
        # ...
        sysinfo = systeminfo.SystemInfo()
        img = os.path.join('/usr/share/pixmaps', f'{sysinfo.name_id}.png')
        if not os.path.isfile(img):
            img = os.path.join(self.__base_dir, 'resources', 'linux.png')

        return ansicolorimage.AnsiColorImage(
            url_image=img, contrast=1.3, brightness=0.85)

    def __get_infos(self) -> list:
        # ...
        info = ''
        _cmd = subprocess.Popen(
            ['tput', 'cols'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tput_cols, _stderr = _cmd.communicate()

        system_info_items = formattedsysteminfo.FormattedSystemInfo()
        for key, value in system_info_items.system_fetch_as_dict.items():
            value_width = int(tput_cols) - len(key) - self.__logo.width - 3

            if len(value) > value_width:
                info += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__logo.image_accent_color,
                    key,
                    value[:value_width - 3] + '...')
            else:
                info += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__logo.image_accent_color, key, value)

        return info.split('\n')

    def __set_same_amount_of_lines_for_logo_and_info(self) -> None:
        # Same height
        len_image = len(self.__logo.ansi_lines)
        len_info = len(self.__infos)

        bar = colorbar.ColorBar(self.__logo.image_accent_color.split(';'))
        color_bar = bar.colorbar

        if len_image < len_info:
            self.__infos[-1] = color_bar
            for _ in range(len_info - len_image):
                self.__logo.ansi_lines.append(' ' * self.__logo.width)
        else:
            for _ in range(len_image - len_info):
                self.__infos.append(' ')

            self.__infos[-1] = color_bar


def main() -> None:
    """..."""
    info = SystemInfo()
    info.fetch()


if __name__ == '__main__':
    main()
