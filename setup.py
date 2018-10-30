#!/usr/bin/env python3

from distutils.core import setup
import os
import shutil


PO_DIR     = 'po'
LOCALE_DIR = 'locale'
APP_ID     = 'indicator-docker'


def compile_lang_files() -> list:
    """(Re)generate .mo files from the available .po files, if any.
    :return: a list of .mo files to be packaged or installed
    """
    # Get a canonical locale path
    locale_dir = os.path.abspath(LOCALE_DIR)

    # Installing/packaging from the source tree (the 'po' dir is available): compile .po into .mo
    if os.path.isdir(PO_DIR):
        # Get a canonical path to the .po dir
        po_dir = os.path.abspath(PO_DIR)
        # Remove the locale dir altogether, if any
        if os.path.isdir(locale_dir):
            shutil.rmtree(locale_dir)
        # Create a new dir
        os.makedirs(locale_dir)
        # Iterate through available .po files
        for in_file in os.listdir(po_dir):
            if in_file.endswith('.po'):
                # Use the name of .po file (without extension) as the language name
                lang = os.path.splitext(in_file)[0]
                # Create a target dir for the .mo file
                mo_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
                os.makedirs(mo_dir)
                # Compile the .po into a .mo
                os.system('msgfmt "{}" -o "{}"'.format(os.path.join(po_dir, in_file), os.path.join(mo_dir, APP_ID + '.mo')))

    # Check a locale dir is there
    if not os.path.isdir(locale_dir):
        print('WARNING: Directory {} doesn\'t exist, no locale files will be included.'.format(locale_dir))
        return []

    # Return all available .mo translation files to the list data files
    return [
        (
            'share/locale/{}/LC_MESSAGES'.format(lang),
            [os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', APP_ID + '.mo')]
        ) for lang in os.listdir(locale_dir)
    ]

data_files = [
    # App shortcut
    ('share/applications',                      [APP_ID+'.desktop']),

    # Autostart entry
    ('/etc/xdg/autostart',                      [APP_ID+'.desktop']),

    # Icons
    ('share/icons/ubuntu-mono-dark/status/22',  ['icons/ubuntu-mono-dark/indicator-docker.svg']),
    ('share/icons/ubuntu-mono-light/status/22', ['icons/ubuntu-mono-light/indicator-docker.svg']),
    ('share/icons/hicolor/22x22/status',        ['icons/default/indicator-docker.svg']),

    # Manpage
    ('share/man/man1',                          ['man/indicator-docker.1']),
]

# Configure
setup(
    name=APP_ID,
    version='0.1.0ubuntu0',
    description='Application indicator to control Docker containers',
    author='Dmitry Kann',
    author_email='yktooo@gmail.com',
    url='https://github.com/yktoo/indicator-docker',
    license='GPL3',
    package_dir={'': 'lib'},
    packages=['indicator_docker'],
    scripts=['indicator-docker'],
    data_files=data_files + compile_lang_files(),
)
