#!/usr/bin/env python3
import sys
import os
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ansi.ansicolorimage
import ansi.colorbar
import info.systeminfo
import info.formattedsysteminfo


class InfoFetch(object):
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
        self.__colorbar = ansi.colorbar.ColorBar(
            self.__logo.image_accent_color.split(';'))

    @property
    def colobar_item_width(self) -> int:
        """..."""
        return self.__colorbar_item_width

    @colobar_item_width.setter
    def colobar_item_width(self, value: int) -> None:
        self.__colorbar_item_width = value
        self.__colorbar.color_item_width = self.__colorbar_item_width

    @property
    def colorbar_is_legacy(self) -> bool:
        """..."""
        return self.__colorbar_is_legacy

    @colorbar_is_legacy.setter
    def colorbar_is_legacy(self, value: bool) -> None:
        self.__colorbar_is_legacy = value
        self.__colorbar.is_legacy = self.__colorbar_is_legacy

    def fetch(self) -> int:
        """..."""
        self.__set_same_amount_of_lines_for_logo_and_info()
        for img_line, text_line in zip(
                self.__logo.ansi_lines, self.__infos):
            print(img_line, text_line)
        return 0

    def __get_logo(self) -> ansi.ansicolorimage:
        # ...
        sysinfo = info.systeminfo.SystemInfo()
        img = os.path.join('/usr/share/pixmaps', f'{sysinfo.name_id}.png')
        if not os.path.isfile(img):
            img = os.path.join(self.__base_dir, 'resources', 'linux.png')

        return ansi.ansicolorimage.AnsiColorImage(
            url_image=img, contrast=1.3, brightness=0.85)

    def __get_infos(self) -> list:
        # ...
        infos = ''
        _cmd = subprocess.Popen(
            ['tput', 'cols'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tput_cols, _stderr = _cmd.communicate()

        system_info_items = info.formattedsysteminfo.FormattedSystemInfo()
        for key, value in system_info_items.system_fetch_as_dict.items():
            value_width = int(tput_cols) - len(key) - self.__logo.width - 3

            if len(value) > value_width:
                infos += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__logo.image_accent_color,
                    key,
                    value[:value_width - 3] + '...')
            else:
                infos += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__logo.image_accent_color, key, value)

        return infos.split('\n')

    def __set_same_amount_of_lines_for_logo_and_info(self) -> None:
        # Same height
        len_image = len(self.__logo.ansi_lines)
        len_info = len(self.__infos)

        if len_image < len_info:
            self.__infos[-1] = self.__colorbar.colorbar
            for _ in range(len_info - len_image):
                self.__logo.ansi_lines.append(' ' * self.__logo.width)
        else:
            for _ in range(len_image - len_info):
                self.__infos.append(' ')

            self.__infos[-1] = self.__colorbar.colorbar


def main() -> None:
    """..."""
    infofetch = InfoFetch()
    infofetch.fetch()


if __name__ == '__main__':
    main()
