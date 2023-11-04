#!/usr/bin/env python3
import systeminfo


class FormattedSystemInfo(object):
    """Create an object of type 'InfoFetch'

    It gives access to various information about the
    operating system, such as architecture, memory, cpu...
    """

    def __init__(self) -> None:
        """..."""
        self.__sys_info = systeminfo.SystemInfo()
        self.__system_fetch_as_dict = None

    @property
    def system_fetch_as_dict(self) -> dict:
        """..."""
        if not self.__system_fetch_as_dict:
            self.__system_fetch_as_dict = {
                'OS': self.__format_os_name(),
                'Kernel': self.__format_kernel(),
                'User': self.__format_user(),
                'Hostname': self.__sys_info.hostname,
                'DE': self.__format_desktop_environment(),
                'WM': self.__format_window_manager(),
                'Display server': self.__format_display_server(),
                'Style theme': self.__format_style_theme(),
                'Icons theme': self.__format_icons_theme(),
                'Packages': self.__format_packages(),
                'Shell': self.__format_shell(),
                'Uptime': self.__format_uptime(),
                'Board': self.__format_motherboard(),
                'CPU': self.__format_cpu(),
                'GPU': self.__format_gpu(),
                'RAM': self.__format_ram(),
                'Swap': self.__format_swap(),
                'Resolution': self.__format_resolution()}

        return self.__system_fetch_as_dict

    def __format_user(self) -> str | None:
        # ...
        user = self.__sys_info.username
        username = self.__sys_info.user_name
        if user and username:
            return f'{user} [{username}]'
        if user:
            return f'{user}'
        return None

    def __format_os_name(self) -> str | None:
        # ...
        os_pretty_name_ = self.__sys_info.pretty_name
        name = (
            os_pretty_name_ if os_pretty_name_ else
            self.__sys_info.name + '' + self.__sys_info.get_version())
        os_name = name + ' ' + self.__sys_info.codename

        if not os_name and not os_pretty_name_:
            return None

        return os_name

    def __format_kernel(self) -> str | None:
        # ...
        kernel = self.__sys_info.get_kernel()
        if kernel:
            kernel = f'{kernel} {self.__sys_info.get_kernel_version()}'

        architecture = self.__sys_info.get_kernel_architecture()
        if kernel and architecture:
            kernel = f'{kernel} [{architecture} bits]'

        return kernel if kernel else None

    def __format_motherboard(self) -> str | None:
        # ...
        motherboard = self.__sys_info.get_motherboard()
        motherboard_version = self.__sys_info.get_motherboard_version()

        if motherboard and motherboard_version:
            return '{} - {}'.format(motherboard, motherboard_version)

        elif motherboard and not motherboard_version:
            return motherboard

        else:
            return None

    def __format_cpu(self) -> str | None:
        # ...
        cpu = self.__sys_info.get_cpu()
        architecture = self.__sys_info.get_cpu_architecture()

        if cpu and architecture:
            cpu = f'{cpu} [{architecture}]'

        return cpu if cpu else None

    def __format_gpu(self) -> str | None:
        # ...
        gpu = self.__sys_info.get_gpu()
        return gpu if gpu else None

    def __format_ram(self) -> str | None:
        # ...
        ram = self.__sys_info.get_ram()
        used = self.__sys_info.get_ram_used()
        free = self.__sys_info.get_ram_free()
        return (
            '{}, {} used, {} free'.format(ram, used, free)
            if ram else None)

    def __format_swap(self) -> str | None:
        # ...
        swap = self.__sys_info.get_swap()
        used = self.__sys_info.get_swap_used()
        free = self.__sys_info.get_swap_free()
        return (
            '{}, {} used, {} free'.format(swap, used, free)
            if swap else None)

    def __format_resolution(self) -> str | None:
        # ...
        resolution = self.__sys_info.get_screen_resolution()
        return resolution if resolution else None

    def __format_uptime(self) -> str | None:
        # ...
        uptime = self.__sys_info.get_uptime()
        return uptime if uptime else None

    def __format_shell(self) -> str | None:
        # ...
        shell = self.__sys_info.get_shell()

        if 'bash' in shell.lower():
            shell = 'Bash'
        return shell if shell else None

    def __format_desktop_environment(self) -> str | None:
        # ...
        _de = self.__sys_info.get_desktop_environment()
        _de_version = self.__sys_info.get_desktop_environment_version()

        de = _de if _de else ''
        de_version = _de_version if _de_version else ''

        if de_version:
            de = de + ' ' + de_version
        return de if de else None

    def __format_window_manager(self) -> str | None:
        # ...
        wm = self.__sys_info.get_window_manager()
        return wm if wm else None

    def __format_display_server(self) -> str | None:
        # ...
        ds = self.__sys_info.get_display_server()
        return ds if ds else None

    def __format_style_theme(self) -> str | None:
        # ...
        style = []

        qt_style = self.__sys_info.kde_style
        if qt_style:
            style.append(f'Qt={qt_style}')

        gtk_style = self.__sys_info.gtk_style
        if gtk_style:
            style.append(f'Gtk={gtk_style}')

        return ', '.join(style)

    def __format_icons_theme(self) -> str | None:
        # ...
        icons = []

        qt_icons = self.__sys_info.kde_icons
        if qt_icons:
            icons.append(f'Qt={qt_icons}')

        gtk_icons = self.__sys_info.gtk_icons
        if gtk_icons:
            icons.append(f'Gtk={gtk_icons}')

        return ', '.join(icons)

    def __format_packages(self) -> str:
        # ...

        # Native
        str_num_native_packages = self.__sys_info.get_packages()
        native_packages_name = self.__sys_info.get_package_manager()

        # Total packages
        total_packages = str_num_native_packages

        # Return var
        packages = '{} {}'.format(total_packages, native_packages_name)

        # If Flatpak or snap
        str_num_flatpak_packages = self.__sys_info.get_flatpak_packages()
        str_num_snap_packages = self.__sys_info.get_snap_packages()

        if str_num_flatpak_packages or str_num_snap_packages:
            # Only Flatpak
            if str_num_flatpak_packages and not str_num_snap_packages:
                total_packages = (str(
                    int(str_num_flatpak_packages)
                    + int(str_num_native_packages)))

                packages = '{} {}={}, flatpak={}'.format(
                    total_packages, native_packages_name,
                    str_num_native_packages, str_num_flatpak_packages)

            # Only Snap
            elif not str_num_flatpak_packages and str_num_snap_packages:
                total_packages = (str(
                    int(str_num_snap_packages) + int(str_num_native_packages)))

                packages = '{} {}={}, snap={}'.format(
                    total_packages, native_packages_name,
                    str_num_native_packages, str_num_snap_packages)

            # Flatpak and Snap
            else:
                total_packages = str(
                    int(str_num_flatpak_packages)
                    + int(str_num_snap_packages)
                    + int(str_num_native_packages))

                packages = '{} {}={}, flatpak={}, snap={}'.format(
                    total_packages, native_packages_name,
                    str_num_native_packages, str_num_flatpak_packages,
                    str_num_snap_packages)

        return packages


if __name__ == '__main__':
    print('Resume system info:')
    fsi = FormattedSystemInfo()
    for k, v in fsi.system_fetch_as_dict.items():
        print(k, '->', v)
