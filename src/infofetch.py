#!/usr/bin/env python3
import sys
import os
import subprocess

from xdg import IconTheme
import cairosvg

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ansi.ansicolorimage
import ansi.colorbar
import info.systeminfo
import info.formattedsysteminfo
import info.desktopentryparse


class InfoFetch(object):
    """..."""

    def __init__(self) -> None:
        """..."""
        self.__base_dir = os.path.dirname(os.path.abspath(__file__))
        self.__sys_info = info.formattedsysteminfo.FormattedSystemInfo()

        self.__logo_height = 20
        self.__logo_width = 20
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

    @property
    def colorbar_is_mirrored(self) -> bool:
        """..."""
        return self.__colorbar_is_mirrored

    @colorbar_is_mirrored.setter
    def colorbar_is_mirrored(self, value: bool) -> None:
        self.__colorbar_is_mirrored = value
        self.__colorbar.is_mirrored = self.__colorbar_is_mirrored

    def fetch(self) -> int:
        """..."""
        self.__set_same_amount_of_lines_for_logo_and_info()
        for img_line, text_line in zip(
                self.__logo.ansi_lines, self.__infos):
            print(img_line, text_line)
        return 0

    def __get_logo(self) -> ansi.ansicolorimage:
        # ...
        img_path = ''
        logo_id = info.desktopentryparse.DesktopFile(
            os.path.join(self.__base_dir, 'statics', 'logobyidrc'))

        # Statics
        if not img_path:
            if self.__sys_info.raw_info.name_id.lower() in logo_id.content[
                    '[Logos]']:
                img_name = logo_id.content['[Logos]'][
                    self.__sys_info.raw_info.name_id.lower()]
                img_path = os.path.join(self.__base_dir, 'statics', img_name)

        # Pixmaps
        if not os.path.isfile(img_path):
            for objfile in os.listdir('/usr/share/pixmaps'):
                if self.__sys_info.raw_info.name_id.lower() in objfile.lower():
                    if objfile.endswith('.png'):
                        img_path = os.path.join('/usr/share/pixmaps', objfile)
                        break

        # Icon theme
        if not os.path.isfile(img_path):
            icons = self.__sys_info.raw_info.kde_icons
            if not icons:
                icons = self.__sys_info.raw_info.gtk_icons
            if icons:
                if 'LOGO' in self.__sys_info.raw_info.os_release:
                    img_path = IconTheme.getIconPath(
                        self.__sys_info.raw_info.os_release['LOGO'],
                        theme=self.__sys_info.raw_info.kde_icons)

                    if img_path and img_path.endswith('.svg'):
                        cairosvg.svg2png(
                            url=img_path,
                            write_to=f'/tmp/infofetch-logo.png',
                            output_width=self.__logo_width,
                            output_height=self.__logo_height)

                        img_path = '/tmp/infofetch-logo.png'

                    if not img_path:
                        img_path = ''

        # Default
        if not os.path.isfile(img_path):
            img_path = os.path.join(self.__base_dir, 'statics', 'linux.png')

        return ansi.ansicolorimage.AnsiColorImage(
            url_image=img_path, contrast=1.3, brightness=0.85)

    def __get_infos(self) -> list:
        # ...
        infos = ''
        _cmd = subprocess.Popen(
            ['tput', 'cols'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        tput_cols, _stderr = _cmd.communicate()

        color_4_value_start, color_4_value_end = '', ''
        if self.__sys_info.raw_info.name_id == 'manjaro':
            color_4_value_start = '\x1b[38;2;200;200;200m'
            color_4_value_end = '\x1B[0m'

        for key, value in self.__sys_info.info_fetch_as_dict.items():
            value_width = int(tput_cols) - len(key) - self.__logo.width - 3

            if value:
                if len(value) > value_width:
                    infos += "\x1b[38;2;{}m{}\x1B[0m{}: {}{}\n".format(
                        self.__logo.image_accent_color,
                        key,
                        color_4_value_start,
                        value[:value_width - 3] + '...',
                        color_4_value_end)
                else:
                    infos += "\x1b[38;2;{}m{}\x1B[0m{}: {}{}\n".format(
                        self.__logo.image_accent_color, key,
                        color_4_value_start, value, color_4_value_end)

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
