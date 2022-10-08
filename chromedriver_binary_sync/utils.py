# coding: utf-8
"""
Helper functions for filename and URL generation.

Copyright (c) 2022 Daniel Kaiser | MIT License
Copyright (c) 2022 bugph0bia | MIT License
- Daniel Kaiser: make "utils.py" original version. ("https://pypi.org/project/chromedriver-binary-auto/")
- bugph0bia: copy to this project.
- bugph0bia: change get_chrome_major_version() func, add code for GoogleChromePortable on Windows.
"""

import sys
import os
import subprocess
import re
import platform
import glob

try:
    from urllib.request import urlopen, URLError
except ImportError:
    from urllib2 import urlopen, URLError

__author__ = 'Daniel Kaiser <d.kasier@fz-juelich.de>'


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith('win'):
        return 'chromedriver.exe'
    return 'chromedriver'


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith('win'):
        return ';'
    return ':'


def get_chromedriver_url(version):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: chromedriver version string
    :return: Download URL for chromedriver
    """
    base_url = 'https://chromedriver.storage.googleapis.com/'
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        _platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        _platform = 'mac'
        architecture = '64'
        if platform.machine() == 'arm64':
            architecture += '_m1'
    elif sys.platform.startswith('win'):
        _platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return base_url + version + '/chromedriver_' + _platform + architecture + '.zip'


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if 'PATH' not in os.environ:
        return None
    for directory in os.environ['PATH'].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def get_latest_release_for_version(version=None):
    """
    Searches for the latest release (complete version string) for a given major `version`. If `version` is None
    the latest release is returned.
    :param version: Major version number or None
    :return: Latest release for given version
    """
    release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    if version:
        release_url += '_{}'.format(version)
    try:
        response = urlopen(release_url)
        if response.getcode() != 200:
            raise URLError('Not Found')
        return response.read().decode('utf-8').strip()
    except URLError:
        raise RuntimeError('Failed to find release information: {}'.format(release_url))


def get_chrome_major_version(chrome_portable=None):
    """
    Detects the major version number of the installed chrome/chromium browser.
    :param chrome_portable: Path when using GoogleChromePortable (Windows only)
    :return: The browsers major version number or None
    """
    # Windows
    if sys.platform.startswith('win'):
        # chrome.exe path
        if chrome_portable:
            browser_executables = [chrome_portable]
        else:
            browser_executables = [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                                   r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe']
        # get chrome versions
        majors = []
        for browser_executable in browser_executables:
            # Get the version from the folder name of the version in the same location as chrome.exe.
            for sibling in glob.glob(os.path.dirname(browser_executable) + r'\*.*.*.*'):
                # get major version
                if major := re.match(r'(?P<major>\d+)\.(\d+)\.(\d+)\.(\d+)', os.path.basename(sibling)).group('major'):
                    majors.append(major)
        # returns highest version.
        sorted(majors)
        return majors[-1]

    # Linux, Mac
    else:
        browser_executables = ['google-chrome', 'chrome', 'chrome-browser', 'google-chrome-stable', 'chromium', 'chromium-browser']
        if sys.platform == "darwin":
            browser_executables.insert(0, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        for browser_executable in browser_executables:
            try:
                version = subprocess.check_output([browser_executable, '--version'])
                return re.match(r'.*?((?P<major>\d+)\.(\d+\.){2,3}\d+).*?', version.decode('utf-8')).group('major')
            except Exception:
                pass


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, '-v'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print(get_chromedriver_path())
