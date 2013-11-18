# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'path': sys.path + ['../src/'],
        'includes': [
            'DiffUtil',
            'ClearCaseConnecter'
        ],
        "create_shared_zip": False,
        'include_files': [("../src/config.ini","")],
        'append_script_to_exe': True
    }
}

executables = [
    Executable('../src/CommitCC.py')
]

setup(name='CommitCC',
      version='0.1',
      description='Auto Commit Tool For ClearCase.',
      options=options,
      executables=executables
      )
