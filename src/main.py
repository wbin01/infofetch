#!/usr/bin/env python3
import os

import ansicolorimage
import systeminfo


# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# /usr/share/pixmaps/neon.png

class SystemInfo(object):
    """..."""

    def __init__(self) -> None:
        """..."""
        self.__height = 25
        self.__width = 50
        self.__base_dir = os.path.dirname(os.path.abspath(__file__))
        self.__os_informations = self.__get_system_info()
        self.__os_logo = self.__get_system_logo()

    def fetch(self) -> None:
        """..."""
        self.__set_same_amount_of_lines_for_logo_and_info()

        for img_line, text_line in zip(
                self.__os_logo.ansi_lines, self.__os_informations):
            print(img_line, '\x1b[38;2;{}m{}\x1B[0m'.format(
                self.__os_logo.image_accent_color, text_line))

    def __get_system_logo(self) -> ansicolorimage:
        # test
        return ansicolorimage.AnsiColorImage(
            url_image=os.path.join(self.__base_dir, 'resources', 'neon.png'),
            contrast=1.3, brightness=0.85)

    @staticmethod
    def __get_system_info() -> list:
        # test
        text = ''
        df = systeminfo.ResumeSystemInfo()
        for k, v in df.get_distro_info().items():
            text += f'\n{k}: {v}'
        # text = ('10\n' * 10).split()

        return text.split('\n')

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
