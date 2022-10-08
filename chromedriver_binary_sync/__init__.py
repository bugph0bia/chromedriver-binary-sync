"""
Module file of chromedriver_binary_sync.

Copyright (c) 2022 Daniel Kaiser | MIT License
Copyright (c) 2022 bugph0bia | MIT License
- Daniel Kaiser: make "setup.py". ("https://pypi.org/project/chromedriver-binary-auto/")
- bugph0bia: copy to this project parts of code in "setup.py".
- bugph0bia: change "get_chrome_major_version()" func, add code for GoogleChromePortable on Windows.
"""

import os
import shutil
import zipfile

try:
    from io import BytesIO
    from urllib.request import urlopen, URLError
except ImportError:
    from StringIO import StringIO as BytesIO
    from urllib2 import urlopen, URLError

from .utils import get_chromedriver_filename, get_chromedriver_url, find_binary_in_path, \
    check_version, get_chrome_major_version, get_latest_release_for_version

# clear installation path that automatically added to
# the PATH environment variable by chromedriver_binary.
path = os.environ['PATH'] if 'PATH' in os.environ else None
import chromedriver_binary
if path:
    os.environ['PATH'] = path
else:
    os.environ.pop('PATH')


def download(download_dir='.', chrome_portable=None, verbose=False):
    """
    Downloads, unzips and installs chromedriver.
    If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.
    :param download_dir: The directory to download. (default: current directory)
    :param chrome_portable: File path if you are using the portable version of Chrome.
    :param verbose: Verbose mode. (print log)
    :return: chromedriver path
    """
    # get installed chrome version
    chrome_major = get_chrome_major_version(chrome_portable)
    chromedriver_version = get_latest_release_for_version(chrome_major)
    vprint(verbose, f'Chrome major version (installed): {chrome_major}')
    vprint(verbose, f'Chromedriver version (to be download): {chromedriver_version}')

    # download chromedriver
    chromedriver_dir = os.path.abspath(download_dir)
    chromedriver_filename = find_binary_in_path(get_chromedriver_filename())

    # copy if already installed to a location with PATH
    if chromedriver_filename and check_version(chromedriver_filename, chromedriver_version):
        vprint(verbose, f'Chromedriver already installed at {chromedriver_filename}...')
        new_filename = os.path.join(chromedriver_dir, get_chromedriver_filename())
        if chromedriver_filename.lower() != new_filename.lower():
            shutil.copy2(chromedriver_filename, new_filename)
            vprint(verbose, 'Chromedriver copied.')

    else:
        # download path of chromedriver
        chromedriver_bin = get_chromedriver_filename()
        chromedriver_filename = os.path.join(chromedriver_dir, chromedriver_bin)

        # download the required version of chromedriver if it does not exist
        if not os.path.isfile(chromedriver_filename) or not check_version(chromedriver_filename, chromedriver_version):
            vprint(verbose, 'Downloading Chromedriver...')
            if not os.path.isdir(chromedriver_dir):
                os.mkdir(chromedriver_dir)
            url = get_chromedriver_url(version=chromedriver_version)
            try:
                response = urlopen(url)
                if response.getcode() != 200:
                    raise URLError('Not Found')
            except URLError:
                raise RuntimeError('Failed to download chromedriver archive: {}'.format(url))

            # unzip
            archive = BytesIO(response.read())
            with zipfile.ZipFile(archive) as zip_file:
                zip_file.extract(chromedriver_bin, chromedriver_dir)
        else:
            vprint(verbose, f'Chromedriver already installed at {chromedriver_filename}...')

        # set permission
        if not os.access(chromedriver_filename, os.X_OK):
            os.chmod(chromedriver_filename, 0o744)

    return chromedriver_filename


def vprint(verbose, text):
    if verbose:
        print(text)
