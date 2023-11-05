#!/usr/bin/env python3
import os
import re
import subprocess

import desktopentryparse


class SystemInfo(object):
    """Create an object of type 'LinuxInfo'

    Gets information about the operating system.
    """
    def __init__(self):
        """Class constructor

        This object contains a lot of information, so, to keep it light,
        all properties start out empty and are filled in as the accessor
        methods are used.
        """
        self.__user_name = None
        self.__username = None
        self.__hostname = None
        self.__os_release = self.os_release
        self.__pretty_name = None
        self.__name = None
        self.__name_id = None
        self.__codename = None
        self.__version = None
        self.__kernel = None
        self.__kernel_version = None
        self.__kernel_architecture = None
        self.__motherboard = None
        self.__motherboard_version = None
        self.__cpu = None
        self.__cpu_architecture = None
        self.__gpu = None
        self.__ram = self.ram
        self.__ram_used = None
        self.__ram_free = None
        self.__swap = None
        self.__swap_used = None
        self.__swap_free = None
        self.__screen_resolution = None
        self.__uptime = None
        self.__shell = None
        self.__desktop_environment = None
        self.__desktop_environment_version = None
        self.__window_manager = None
        self.__package_manager = None
        self.__display_server = None
        self.__packages = None
        self.__flatpak_packages = None
        self.__snap_packages = None
        self.__kde_style = None
        self.__kde_icons = None
        self.__gtk_style = None
        self.__gtk_icons = None

    @property
    def user_name(self) -> str | None:
        """The name of the user

        The correct name that the user registered, not the 'username'.

        :return: String containing the name of the user
        """
        if self.__user_name:
            return self.__user_name

        user_name = subprocess.getoutput(
            "cat /etc/passwd | grep `echo $HOME` | awk -F ':' '{print $5}'"
        ).strip()
        self.__user_name = user_name if user_name else None

        return self.__user_name

    @property
    def username(self) -> str | None:
        """The username

        The username used to log in, not the correct or correctly
        formatted name.

        :return: String containing username
        """
        if self.__username:
            return self.__username

        username = os.environ['USER'].strip()
        self.__username = username if username else None

        return self.__username

    @property
    def hostname(self) -> str | None:
        """The host name

        The recognition name on the network.

        :return: String containing the hostname
        """
        if self.__hostname:
            return self.__hostname

        # Fix $HOSTNAME missing
        if subprocess.getoutput('cat /etc/hostname ; echo $?')[-1] == '0':
            hostname = subprocess.getoutput('cat /etc/hostname')
        else:
            hostname = subprocess.getoutput('echo $HOSTNAME')

        # Fix $HOSTNAME in Fedora
        if 'fedora' in self.name.lower():
            hostname = subprocess.getoutput('printf "${HOSTNAME%%.*}"')

        self.__hostname = hostname.strip() if hostname.strip() else None
        return self.__hostname

    @property
    def os_release(self) -> dict:
        """cat /etc/os-release

        All information from the '/etc/os-release' file in a dictionary.

        :return: Dict containing information from the '/etc/os-release' file
        """
        all_release_info = {}

        cat_release = subprocess.getoutput('cat /etc/os-release').split('\n')
        for item_release in cat_release:
            items = item_release.split('=')
            all_release_info[items[0]] = items[1].strip('"').strip("'")

        # HACK: Identify some known distributions that do not configure
        # version information as they should
        hack_name = False
        name = str()
        name_id = str()

        if 'ubuntu' in all_release_info['NAME'].lower():
            # Lubuntu
            if 'openbox' in subprocess.getoutput('ls /usr/share/lubuntu/'):
                hack_name = True
                name = 'Lubuntu'
                name_id = 'lubuntu'

            # ubuntu Budgie
            elif 'Budgie Welcome' in subprocess.getoutput(
                    'ubuntu-budgie-welcome.budgie-welcome --version'):
                hack_name = True
                name = 'Ubuntu Budgie'
                name_id = 'ubuntubudgie'

            # Xubuntu
            elif 'applications' in subprocess.getoutput(
                    'ls /usr/share/xubuntu/'):
                hack_name = True
                name = 'Xubuntu'
                name_id = 'xubuntu'

        if hack_name:
            all_release_info['NAME'] = name
            all_release_info['ID'] = name_id
            if 'PRETTY_NAME' in all_release_info:
                all_release_info['PRETTY_NAME'] = all_release_info[
                    'PRETTY_NAME'].replace('Ubuntu', name)

        self.__os_release = all_release_info
        return self.__os_release

    @property
    def pretty_name(self) -> str | None:
        """Verbally formatted name

        The pretty name in the '/etc/os-release' file.

        :return: String containing pretty name
        """
        if self.__pretty_name:
            return self.__pretty_name

        self.__pretty_name = (self.__os_release['PRETTY_NAME']
                              if 'PRETTY_NAME' in self.__os_release else None)

        return self.__pretty_name

    @property
    def name(self) -> str | None:
        """Operating system name

        The commercially formatted name, which can contain uppercase letters
        and spaces.

        :return: String containing the name of the operating system
        """
        if self.__name:
            return self.__name

        self.__name = (self.__os_release['NAME']
                       if 'NAME' in self.__os_release else None)
        return self.__name

    @property
    def name_id(self) -> str | None:
        """Operating system identity

        The identifier formatted name for code or database; usually in
        lowercase and without spaces.

        :return: String containing the operating system ID
        """
        if self.__name_id:
            return self.__name_id

        name_id = ''
        if 'ID' in self.__os_release:
            name_id = self.__os_release['ID']
        elif 'NAME' in self.__os_release:
            name_id = self.__os_release['NAME'].lower()

        self.__name_id = name_id.strip() if name_id.strip() else None
        return self.__name_id

    @property
    def codename(self) -> str | None:
        """Operating system codename

        The code name is the commercial one, to easily identify the versions 
        of the operating system.
        Not all systems do.

        :return: String containing the codename of the operating system
        """
        if self.__codename:
            return self.__codename

        codename = ''
        if 'VERSION_CODENAME' in self.__os_release:
            codename = self.__os_release['VERSION_CODENAME']
        elif 'CODENAME' in self.__os_release:
            codename = self.__os_release['CODENAME']
        self.__codename = codename.strip() if codename.strip() else None

        return self.__codename

    @property
    def version(self) -> str | None:
        """Operating system version

        The current version of the operating system.

        :return: String containing the version of the operating system
        """
        if self.__version:
            return self.__version

        version = ''
        if 'VERSION_ID' in self.__os_release:
            version = self.__os_release['VERSION_ID']
        elif 'VERSION' in self.__os_release:
            version = self.__os_release['VERSION']
        self.__version = version.strip() if version.strip() else None

        return self.__version

    @property
    def kernel(self) -> str | None:
        """Operating system kernel name

        The current operating system kernel.

        :return: String containing the kernel name
        """
        if self.__kernel:
            return self.__kernel

        kernel = subprocess.getoutput(
            'cat /proc/sys/kernel/ostype').title().strip()
        self.__kernel = kernel if kernel else None

        return self.__kernel

    @property
    def kernel_version(self) -> str | None:
        """Operating system kernel version

        The current kernel version of the operating system.

        :return: String containing the kernel version
        """
        if self.__kernel_version:
            return self.__kernel_version

        regex = re.compile(r'(\.x\d.+|x\d.+)')
        kernel_version = regex.sub(
            '', subprocess.getoutput('cat /proc/sys/kernel/osrelease')).strip()
        self.__kernel_version = kernel_version if kernel_version else None

        return self.__kernel_version

    @property
    def kernel_architecture(self) -> str | None:
        """..."""
        if self.__kernel_architecture:
            return self.__kernel_architecture

        architecture = subprocess.getoutput(
            'getconf LONG_BIT').title().strip()
        self.__kernel_architecture = architecture if architecture else None
        return self.__kernel_architecture

    @property
    def motherboard(self) -> str | None:
        """..."""
        if self.__motherboard:
            return self.__motherboard

        motherboard = subprocess.getoutput(
            'cat /sys/devices/virtual/dmi/id/product_name').strip()
        self.__motherboard = motherboard if motherboard else None

        return self.__motherboard

    @property
    def motherboard_version(self) -> str | None:
        """..."""
        if self.__motherboard_version:
            return self.__motherboard_version

        version = subprocess.getoutput(
            'cat /sys/devices/virtual/dmi/id/product_version').strip()
        self.__motherboard_version = version if version else None

        return self.__motherboard_version

    @property
    def cpu(self) -> str | None:
        """..."""
        if self.__cpu:
            return self.__cpu

        cpu = subprocess.getoutput(
            "cat /proc/cpuinfo | grep 'model name' | "
            "sed -n 1p | sed 's/.*:.//g;s/(\w*)//g'").strip()
        self.__cpu = cpu if cpu else None

        return self.__cpu

    @property
    def cpu_architecture(self) -> str | None:
        """..."""
        if self.__cpu_architecture:
            return self.__cpu_architecture

        cpu = subprocess.getoutput(
            "lscpu | grep Architecture | awk '{print $2}'").strip()
        self.__cpu_architecture = cpu if cpu else None

        return self.__cpu_architecture

    @property
    def gpu(self) -> str | None:
        """..."""
        if self.__gpu:
            return self.__gpu

        gpu = ''
        found = False

        # 1° method ||| dica para achar os drivers: lspci -v
        gpuread = subprocess.getoutput('lspci | grep 3D')
        if 'lspci:' not in gpuread and '/bin/sh:' not in gpuread and gpuread:
            regex = re.findall(r'^.+: (.+) \(rev .+$', gpuread)
            if regex:
                gpu = regex[0]
                found = True

        # 2° method
        if not found:
            board = str()
            id_cmd = "lspci |grep -i graphics| awk '{ print $1 }'"
            gpuid = subprocess.getoutput(id_cmd)
            if gpuid.replace(':', '').replace('.', '').isdigit():
                gpu_cmd = f'cat "/sys/bus/pci/devices/0000:{gpuid}/label"'
                gpu_board = subprocess.getoutput(gpu_cmd).strip()
                board = gpu_board if 'cat: ' not in gpuread else board

            gpuread = subprocess.getoutput('lspci | grep VGA')
            if 'lspci:' in gpuread or '/bin/sh:' in gpuread:
                gpuread = board

            regex = re.findall(r'.+: (.+)', gpuread)
            remove = re.findall(r'\(.+\)', gpuread)
            if regex:
                gpuread = regex[0]
            if remove:
                gpu = gpuread.replace(remove[0], '')

            gpu += board
            found = True

        # Clear
        if found:
            if 'intel' in gpu.lower():
                dirt = [
                    'Corporation',
                    'Core Processor',
                    'Integrated Graphics Controller']
                for i in dirt:
                    gpu = gpu.replace(i, '')

            if 'virtualbox' in gpu.lower():
                gpu = 'VirtualBox Graphics Adapter'
        else:
            gpu = ''

        gpu = gpu.replace('  ', ' ').strip()
        self.__gpu = gpu if gpu else None

        return self.__gpu

    @property
    def ram(self) -> str | None:
        """..."""
        # Somente um método pega todas as informações das memórias
        # para evitar repetir o comando do 'shell'

        # Pegar linhas da memória ram e swap
        memory_info = subprocess.getoutput("free -h")
        memory_info = memory_info.replace(',', '.').split('\n')

        ram_line = memory_info[1].split(' ')  # "memory_info[0]" é o cabeçalho
        swap_line = memory_info[2].split(' ')

        # Lista para armazenar as informações das memórias ram e swap
        ram_info = []
        swap_info = []

        # Preencher as listas com caracteres válidos, removendo vazios
        for ram in ram_line:
            if ram != '':
                ram_info.append(ram.strip())
        for swap in swap_line:
            if swap != '':
                swap_info.append(swap.strip())

        # Atribuir valores da memória ram
        self.__ram = ram_info[1] if ram_info[1] else None
        self.__ram_used = ram_info[2] if ram_info[2] else None
        self.__ram_free = ram_info[3] if ram_info[3] else None
        # Atribuir valores da memória swap
        self.__swap = swap_info[1] if swap_info[1] else None
        self.__swap_used = swap_info[2] if swap_info[2] else None
        self.__swap_free = swap_info[3] if swap_info[3] else None

        return self.__ram

    @property
    def ram_used(self) -> str | None:
        """..."""
        # Already updated in self.ram
        return self.__ram_used

    @property
    def ram_free(self) -> str | None:
        """..."""
        # Already updated in self.ram
        return self.__ram_free

    @property
    def swap(self) -> str | None:
        """..."""
        # Already updated in self.ram
        return self.__swap

    @property
    def swap_used(self) -> str | None:
        """..."""
        # Already updated in self.ram
        return self.__swap_used

    @property
    def swap_free(self) -> str | None:
        """..."""
        # Already updated in self.ram
        return self.__swap_free

    def get_screen_resolution(self) -> str:
        """..."""
        if self.__screen_resolution:
            return self.__screen_resolution

        if subprocess.getoutput('xrandr ; echo $?')[-1] == '0':
            resolution = subprocess.getoutput(
                "xrandr | grep current | awk -F , '{print $2}'")
            self.__screen_resolution = resolution.replace(
                ' current ', '').replace(' x ', 'x')

        return self.__screen_resolution

    def get_uptime(self) -> str:
        """..."""
        if self.__uptime:
            return self.__uptime

        uptime = subprocess.getoutput('uptime -p')
        if uptime[:7] == 'uptime:':
            self.__uptime = subprocess.getoutput(
                'uptime').split(',')[0][9:].replace('up', '').strip() + ' Hs'
        else:
            self.__uptime = uptime.replace('up ', '')

        return self.__uptime

    def get_shell(self) -> str:
        """..."""
        if self.__shell:
            return self.__shell

        self.__shell = subprocess.getoutput('basename $SHELL')
        return self.__shell

    def get_desktop_environment(self) -> str:
        """..."""
        if self.__desktop_environment:
            return self.__desktop_environment

        desktop_environment = subprocess.getoutput(
            'echo $XDG_CURRENT_DESKTOP').replace(':', '-').strip()

        # Limpar
        dirt_to_clean = ['(', ')', "'", '"', 'X-']
        for cleaning_item in dirt_to_clean:
            self.__desktop_environment = desktop_environment.replace(
                cleaning_item, '')

        # Customizar
        if 'kde' in self.__desktop_environment.lower():
            self.__desktop_environment = 'Plasma (KDE)'

        return self.__desktop_environment

    def get_desktop_environment_version(self) -> str:
        """..."""
        if self.__desktop_environment_version:
            return self.__desktop_environment_version

        cmd_version = {
            # 'budgie': "budgie-desktop --version | awk '{print $2}'",
            'cinnamon': "cinnamon --version | awk '{print $2}'",
            # deepin
            'gnome': "gnome-shell --version | awk '{print $3}'",
            'kde': "plasmashell --version | awk '{print $2}'",
            # lxde
            'lxqt': "lxqt-about -v | grep liblxqt | awk '{print $2}'",
            # pantheon elementary
            'xfce': "xfce4-about -V | grep xfce4-about | awk '{print $2}'",
        }
        de = self.get_desktop_environment().lower()
        desktop_environment_version = str()
        for cmd_version_key, cmd_version_value in cmd_version.items():
            if cmd_version_key in de:
                desktop_environment_version = subprocess.getoutput(
                    cmd_version_value)
                break

        # Limpar
        dirt_to_clean = ['(', ')', "'", '"', 'X-']
        for cleaning_item in dirt_to_clean:
            self.__desktop_environment_version = (
                desktop_environment_version.replace(cleaning_item, ''))

        # Customizar
        error = ['bash: ', '/bin/sh: ']
        for item_error in error:
            if item_error in self.__desktop_environment_version.lower():
                self.__desktop_environment_version = ''
                break

        return self.__desktop_environment_version

    def get_window_manager(self) -> str:
        """..."""
        if self.__window_manager:
            return self.__window_manager

        cmd_xprop = subprocess.getoutput(
            'xprop -root -notype _NET_SUPPORTING_WM_CHECK')
        cmd_window_manager = subprocess.getoutput(
            'xprop -id {} -notype -len 100 -f _NET_WM_NAME 8t '
            '| grep WM_KEY'.format(
                cmd_xprop.split()[-1])).split('=')[-1].replace('"', '').strip()

        if cmd_window_manager == '':
            cmd_xprop = subprocess.getoutput(
                'xprop -root -notype _NET_SUPPORTING_WM_CHECK')
            cmd_window_manager = subprocess.getoutput(
                'xprop -id {} -notype -len 100 -f _NET_WM_NAME 8t '
                '| grep WM_NAME'.format(
                    cmd_xprop.split()[-1])).split('=')[-1].replace(
                '"', '').strip()

        self.__window_manager = cmd_window_manager.replace(',', ' | ').replace(
            '(', '').replace(')', '')

        if 'xprop:' in cmd_window_manager:
            self.__window_manager = ''

        # Custom
        if self.__window_manager:
            if 'mutter' in self.__window_manager.lower():
                self.__window_manager = 'Mutter'

        return self.__window_manager

    def get_display_server(self) -> str:
        """..."""
        if self.__display_server:
            return self.__display_server

        self.__display_server = subprocess.getoutput('echo $XDG_SESSION_TYPE')

        # Custom
        if 'wayland' in self.__display_server.lower():
            self.__display_server = 'Wayland'

        return self.__display_server

    def get_package_manager(self) -> str:
        """..."""
        if self.__package_manager:
            return self.__package_manager

        cmd_packages = {
            'dpkg': 'dpkg --get-selections | grep -cv deinstall$',
            'rpm': 'rpm -qa | wc -l',
            'pacman': 'pacman -Qq --color never | wc -l',
            'eopkg': 'eopkg list-installed | wc -l',
        }

        for cmd_packages_key, cmd_packages_value in cmd_packages.items():
            number = int(subprocess.getoutput(cmd_packages_value).split()[-1])

            if number > 0:
                self.__package_manager = cmd_packages_key
                self.__packages = str(number)

        return self.__package_manager

    def get_packages(self) -> str:
        """..."""
        if self.__packages:
            return self.__packages

        self.get_package_manager()

        return self.__packages

    def get_flatpak_packages(self) -> str:
        """..."""
        if self.__flatpak_packages:
            return self.__flatpak_packages

        number = int(subprocess.getoutput('flatpak list | wc -l').split()[-1])
        if number > 0:
            self.__flatpak_packages = str(number)

        return self.__flatpak_packages

    def get_snap_packages(self) -> str:
        """..."""
        if self.__snap_packages:
            return self.__snap_packages

        # Remove cabeçalho com: grep -v "^Name"
        # number = int(subprocess.getoutput(
        # 'snap list | grep -v "^Name" | wc -l').split()[-1])

        # Remove cabeçalho com '-1' no fim
        number = int(subprocess.getoutput('snap list | wc -l').split()[-1]) - 1
        if number > 0:
            self.__snap_packages = str(number)

        return self.__snap_packages

    @property
    def kde_style(self) -> str | None:
        """..."""
        if self.__kde_style:
            return self.__kde_style

        kdeglobals = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        if os.path.isfile(kdeglobals):
            kdeglobals_file = desktopentryparse.DesktopFile(kdeglobals)
            if ('[KDE]' in kdeglobals_file.content and
                    'widgetStyle' in kdeglobals_file.content['[KDE]']):
                self.__kde_style = kdeglobals_file.content['[KDE]'][
                    'widgetStyle']

        return self.__kde_style

    @property
    def kde_icons(self) -> str | None:
        """..."""
        if self.__kde_icons:
            return self.__kde_icons

        kdeglobals = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        if os.path.isfile(kdeglobals):
            kdeglobals_file = desktopentryparse.DesktopFile(kdeglobals)
            if ('[Icons]' in kdeglobals_file.content and
                    'Theme' in kdeglobals_file.content['[Icons]']):
                self.__kde_icons = kdeglobals_file.content['[Icons]'][
                    'Theme']

        return self.__kde_icons

    @property
    def gtk_style(self) -> str | None:
        """..."""
        if self.__gtk_style:
            return self.__gtk_style

        gtk_style = subprocess.getoutput(
            'gsettings get org.gnome.desktop.interface gtk-theme').strip("'")
        self.__gtk_style = gtk_style if gtk_style else None

        return self.__gtk_style

    @property
    def gtk_icons(self) -> str | None:
        """..."""
        if self.__gtk_icons:
            return self.__gtk_icons

        gtk_icons = subprocess.getoutput(
            'gsettings get org.gnome.desktop.interface icon-theme').strip("'")
        self.__gtk_icons = gtk_icons if gtk_icons else None

        return self.__gtk_icons


if __name__ == '__main__':
    print('System info:')
    linux_info = SystemInfo()
    print('                  user-name:', linux_info.user_name)
    print('                   username:', linux_info.username)
    print('                   hostname:', linux_info.hostname)
    print('                pretty-name:', linux_info.pretty_name)
    print('                       name:', linux_info.name)
    print('                    name-id:', linux_info.name_id)
    print('                   codename:', linux_info.codename)
    print('                    version:', linux_info.version)
    print('                     kernel:', linux_info.kernel)
    print('             kernel-version:', linux_info.kernel_version)
    print('        kernel-architecture:', linux_info.kernel_architecture)
    print('                motherboard:', linux_info.motherboard)
    print('        motherboard-version:', linux_info.motherboard_version)
    print('                        cpu:', linux_info.cpu)
    print('           cpu-architecture:', linux_info.cpu_architecture)
    print('                        gpu:', linux_info.gpu)
    print('                        ram:', linux_info.ram)
    print('                   ram-used:', linux_info.ram_used)
    print('                   ram-free:', linux_info.ram_free)
    print('                       swap:', linux_info.swap)
    print('                  swap-used:', linux_info.swap_used)
    print('                  swap-free:', linux_info.swap_free)
    print('          screen-resolution:', linux_info.get_screen_resolution())
    print('                     uptime:', linux_info.get_uptime())
    print('                      shell:', linux_info.get_shell())
    print('        desktop-environment:', linux_info.get_desktop_environment())
    print('desktop-environment-version:',
          linux_info.get_desktop_environment_version())
    print('             window-manager:', linux_info.get_window_manager())
    print('             display-server:', linux_info.get_display_server())
    print('            package-manager:', linux_info.get_package_manager())
    print('                   packages:', linux_info.get_packages())
    print('           flatpak-packages:', linux_info.get_flatpak_packages())
    print('              snap-packages:', linux_info.get_snap_packages())
    print('                  kde-style:', linux_info.kde_style)

    print()
    print('OS release:')
    release = linux_info.os_release
    for release_key, release_value in release.items():
        print(release_key, '->', release_value)
