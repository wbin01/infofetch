#!/usr/bin/env python3
import os

import ansicolorimage
import systeminfo
import formattedsysteminfo


# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# /usr/share/pixmaps/neon.png

class SystemInfo(object):
    """..."""

    def __init__(self) -> None:
        """..."""
        self.__height = 25
        self.__width = 50
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
        img = os.path.join(
            '/usr/share/pixmaps',
            f'{sysinfo.get_name_id()}.png')
        if not os.path.isfile(img):
            img = os.path.join(self.__base_dir, 'resources', 'linux.png')

        return ansicolorimage.AnsiColorImage(
            url_image=img, contrast=1.3, brightness=0.85)

    def __get_system_info(self) -> list:
        # ...
        info = ''

        system_info_items = formattedsysteminfo.FormattedSystemInfo()
        for key, value in system_info_items.system_fetch_as_dict.items():
            if key != 'id':
                info += "\x1b[38;2;{}m{}\x1B[0m: {}\n".format(
                    self.__os_logo.image_accent_color, key, value)

        return info.split('\n')

    def __set_same_amount_of_lines_for_logo_and_info(self) -> None:
        # Same height

        len_image = len(self.__os_logo.ansi_lines)
        len_info = len(self.__os_informations)

        if len_image < len_info:
            for _ in range(len_info - len_image):
                self.__os_logo.ansi_lines.append(' ' * self.__os_logo.width)
        else:
            for _ in range(len_image - len_info):
                self.__os_informations.append(' ')


def main() -> None:
    """..."""
    info = SystemInfo()
    info.fetch()


if __name__ == '__main__':
    main()
