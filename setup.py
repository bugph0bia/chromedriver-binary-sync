import setuptools

from __version__ import __version__


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='chromedriver_binary_sync',
    version=__version__,
    author='bugph0bia',
    author_email='',
    description='Installer for chromedriver. (Auto sync version to GoogleChrome)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bugph0bia/chromedriver-binary-sync',
    packages=setuptools.find_packages(),
    license='MIT',
    keywords='',
    classifiers=[
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Installation/Setup",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'chromedriver-binary-auto',
    ],
)
