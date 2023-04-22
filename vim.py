import os
import tempfile
import subprocess
from constants import TARGET
from clipboard import copy
from config import config
from Xlib import X
from time import sleep

def open_vim(self, compile_latex):
    f = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.typ')

    f.write("$  $")
    f.close()

    config['open_editor'](f.name)

    typst = ""
    with open(f.name, 'r') as g:
        typst = g.read().strip()

    os.remove(f.name)

    if typst != "$  $":
        m = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        m.write(config['typst_document'](typst))
        m.close()

        working_directory = tempfile.gettempdir()
        subprocess.run(
            ['typst', 'compile', m.name],
            cwd=working_directory,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if not os.path.exists(f"{m.name}.pdf"):
            printf("Something screwed up in the compilation process")
            return

        subprocess.run(
            ['pdf2svg', f'{m.name}.pdf', f'{m.name}.svg'],
            cwd=working_directory
        )

        with open(f'{m.name}.svg') as svg:
            subprocess.run(
                ['xclip', '-selection', 'c', '-target', TARGET],
                stdin=svg
            )

        # idk why inkscape sometimes doesn't register the clipboard change
        sleep(0.01)
        self.press('v', X.ControlMask)
    self.press('Escape')
