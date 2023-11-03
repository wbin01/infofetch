#!/usr/bin/env python3
from PIL import Image, ImageEnhance
import re
import warnings


class AnsiColorImage(object):
    """ANSI from an image

    Create figures with text characters and ANSI colors from an image file.
    """
    def __init__(
            self,
            url_image: str,
            # Defaults
            brightness: float = 1.0,
            chars_map: list = None,
            contrast: float = 1.0,
            height: int = 20,
            hide_foreground_character: bool = False,
            show_background_color: bool = False,
            width: int = 40) -> None:
        """Class constructor"""
        self.__default_chars_map = [
            ' ', '´', '.', ':', ';', 'i', '/', 'l', 'j', 'h',
            'N', 'S', 'k', 'W', 'M', 'G', '0', '@', '#', '#']
        self.__ansi_lines = []
        self.__brightness = brightness
        self.__chars_map = chars_map if chars_map else self.__default_chars_map
        self.__contrast = contrast
        self.__height = height
        self.__hide_foreground_character = hide_foreground_character
        self.__image_accent_color = None
        self.__show_background_color = show_background_color
        self.__url_image = url_image
        self.__width = width

        self.update_ascii_lines()

    @property
    def ansi_lines(self) -> list:
        """Getter: list
        A list of lines representing the image. Each item is a line.
        This 'property' does not contain 'setter', so use properties like
        'url_image' together with 'update_ascii_lines()' method to
        update the list.
        """
        return self.__ansi_lines

    @property
    def brightness(self) -> float:
        """Getter: float
        Get the image brightness

        Setter: float
        Set the image brightness

        The 'float' 1.3 is like 30% and 0.85 is like -15%.
        Use 'None' to reset. Default is 1.0.
        """
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: float) -> None:
        self.__brightness = brightness if brightness else 1.0

    @property
    def chars_map(self) -> list:
        """Getter: list
        Get the list of characters that can be used to draw the image.

        Setter: list
        Set the list of characters that can be used to draw the image.

        The first characters represent the darkest colors, and the last
        characters in the list represent the lightest colors, so the
        characters in the middle of the list are the halftones, thus forming
        a gradient.
        Normally, for dark colors we use characters with little filling, like
        a dot and a comma, while for lighter colors it's the opposite, like an
        at sign.
        Example:

            [' ', '.', ';', 'n', 's', 'k', '&', '@', '#']
             |___________|  |___________|  |___________|
                  |              |              |
             Dark-shades    Half-tones     Light-shades

         A list of approximately 20 characters or a little longer is ideal.
        """
        return self.__chars_map

    @chars_map.setter
    def chars_map(self, chars_map: list) -> None:
        self.__chars_map = chars_map if chars_map else self.__default_chars_map

    @property
    def contrast(self) -> float:
        """Getter: float
        Get the image contrast

        Setter: float
        Set the image contrast

        The 'float' 1.3 is like 30% and 0.85 is like -15%.
        Use 'None' to reset. Default is 1.0.
        """
        return self.__contrast

    @contrast.setter
    def contrast(self, contrast: float) -> None:
        self.__contrast = contrast if contrast else 1.0

    @property
    def height(self) -> int:
        """Getter: int
        Get height in number of lines

        Setter: int
        Set height in number of lines

        Use 'None' to reset. Default is 20.
        """
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        self.__height = height if height else 20

    @property
    def hide_foreground_character(self) -> bool:
        """Getter: bool
        Get foreground character usage status

        Setter: bool
        Set foreground character usage status

        If set to 'True', the foreground character will be displayed.
        Use 'None' to reset. Default is 'False'.
        """
        return self.__hide_foreground_character

    @hide_foreground_character.setter
    def hide_foreground_character(self, hide: bool) -> None:
        self.__hide_foreground_character = hide

    @property
    def image_accent_color(self) -> str:
        """Getter: str
        Gets the image's accent color as a string with an RGB pattern, and
        values separated by semicolons, such as: '192;0;53'.
        Use with truecolors pattern. Ex:
            "\\x1b[38;2;192;0;53m MY-TEXT-HERE \x1B[0m"

        Understand the color formatting in the link:
            https://github.com/termstandard/colors

        Setter: str
        Set the image's accent color with an RGB pattern string and
        semicolon-separated values such as: '192;0;53'. Any different pattern
        will not change the property value.
        To reset use 'None'.
        If the image is changed, the accent color is automatically updated.
        """
        if self.__image_accent_color:
            return self.__image_accent_color

        # Colors ['red', 'blue', 'black']
        colors_found = []
        for line in self.__ansi_lines:
            colors_found += re.findall('\\x1b\[\d+;\d+;\d+;\d+;\d+m', line)

        # Count {'red': 2, 'blue': 5, 'black': 22}
        colors_count = {}
        for color in colors_found:
            rgb = color[7:-1]  # '\x1b[38;2;0;0;0m'[7:-1] -> '0;0;0'
            r, g, b = rgb.split(';')

            # Remove black and white colors (all combination: rg b, rb g, gb r)
            if (  # 50 Must have 1 color greater than 50
                    (int(r) > 50 or int(g) > 50 or int(b) > 50) and
                    (  # Must have 2 colors smaller than 200
                        (int(r) < 200 and int(g) < 200) or
                        (int(r) < 200 and int(b) < 200) or
                        (int(g) < 200 and int(b) < 200)
                    )
            ):
                if rgb not in colors_count:
                    colors_count[rgb] = 1
                else:
                    colors_count[rgb] += 1

        # Save biggest number color
        saved_color, saved_num = ('255;255;255', 0)
        for color, num in colors_count.items():
            if num > saved_num:
                saved_color, saved_num = (color, num)
        self.__image_accent_color = saved_color

        return self.__image_accent_color

    @image_accent_color.setter
    def image_accent_color(self, color: str) -> None:
        if color:
            regex_color = re.findall('\d+;\d+;\d+', color)
            if regex_color:
                if color == regex_color[0]:
                    self.__image_accent_color = color
            return

        self.__image_accent_color = color

    @property
    def show_background_color(self) -> bool:
        """Getter: bool
        Get background color usage status

        Setter: bool
        Set background color usage status

        If set to 'True', the background color will be displayed.
        Use 'None' to reset. Default is 'False'.
        """
        return self.__show_background_color

    @show_background_color.setter
    def show_background_color(self, show: bool) -> None:
        self.__show_background_color = show

    @property
    def url_image(self) -> str:
        """Getter: str
        Get the image file path

        Setter: str
        Set path of an image file in the operating system

        Don't use very specific usage images format like 'svg'.
        Use common raster images like 'png', 'jpg' and 'jpeg'.
        Prefer 'jpg' images with a black background as they are faster
        and more accurate for conversion.
        'None' has no effect.
        """
        return self.__url_image

    @url_image.setter
    def url_image(self, url_image: str) -> None:
        if url_image:
            self.__url_image = url_image

    @property
    def width(self) -> int:
        """Getter: int
        Get width in number of columns

        Setter: int
        Set width in number of columns

        Use 'None' to reset. Default is 40.
        """
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        self.__width = width if width else 40

    def update_ascii_lines(self) -> None:
        """Update the 'ansi_lines' property

        This method is used to apply changes to property values and will have
        no visible effect if no property has been modified.
        Use the 'ansi_lines' property to get the new updated list.
        """
        # Reset ansi_lines and accent color
        self.__ansi_lines = []
        self.__image_accent_color = None

        # Image
        image = Image.open(self.__url_image, 'r')
        if image.mode != 'RGB':
            warnings.filterwarnings('ignore')  # Fix RGBA warning
            image = image.convert('RGB')

        # Resize
        h, w = image.size
        if h != self.__height or w != self.__width:
            image = image.resize(
                (self.__width, self.__height),
                Image.Resampling.BICUBIC)  # type: ignore

        # Adjust color
        if self.__contrast != 1.0:
            contrast = ImageEnhance.Contrast(image)
            image = contrast.enhance(self.__contrast)
        if self.__brightness != 1.0:
            brightness = ImageEnhance.Brightness(image)
            image = brightness.enhance(self.__brightness)

        # Map
        ascii_line = ''
        loop_count = 0
        line_count = 0
        for pixel in list(image.getdata()):
            # RGB
            if len(pixel) == 3:
                r, g, b = pixel
            else:
                r, g, b, _a = pixel

            # Foreground:
            #     set brightness to find ascii_map char index
            pixel_brightness = (  # brightness: github.com/EbonJaeger/asciifyer
                    (0.2126 * r) + (0.7152 * g) + (0.0722 * b))

            ascii_map_char_index = int(
                    (pixel_brightness / 255.0) * (len(self.__chars_map)))

            foreground_character = ' '
            if not self.__hide_foreground_character:
                foreground_character = self.__chars_map[ascii_map_char_index]

            # Background:
            #     \x1b[48... for background or \x1b[38... for hidden background
            bg_color = 48 if self.__show_background_color else 38
            ascii_line += '{}{}'.format(
                f'\x1b[{bg_color};2;{r};{g};{b}m',
                foreground_character)

            # Loop config
            if loop_count + 1 == self.__width:
                # Update line
                self.__ansi_lines.append(ascii_line + '\x1B[0m')
                line_count += 1

                # Reset
                ascii_line = ''
                loop_count = 0
            else:
                loop_count += 1


if __name__ == '__main__':
    pass
