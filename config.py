import sys
import subprocess
from pathlib import Path

def open_editor(filename):
    subprocess.run([
        'st',
        '-g', '60x5',
        '-c', 'popup-bottom-center',
        '-e', "nvim",
        "-c", 'normal ll',
        "-c", 'startinsert',
        "-c", "highlight Normal ctermbg=016",
        f"{filename}",
    ])

def typst_document(typst):
    return r"""
#set page(
  width: 10cm,
  height: auto,
  margin: (x: 1cm, y: 1cm)
)

""" + typst

config = {
    # For example '~/.config/rofi/ribbon.rasi' or None
    'rofi_theme': None,
    # Font that's used to add text in inkscape
    'open_editor': open_editor,
    'typst_document': typst_document,
}


# From https://stackoverflow.com/a/67692
def import_file(name, path):
    import importlib.util as util
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

CONFIG_PATH = Path('~/.config/inkscape-shortcut-manager').expanduser()

if (CONFIG_PATH / 'config.py').exists():
    userconfig = import_file('config', CONFIG_PATH / 'config.py').config
    config.update(userconfig)
