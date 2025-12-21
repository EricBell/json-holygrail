from setuptools import setup
from setuptools.command.build_py import build_py
import shutil
import os

class CustomBuildPy(build_py):
    def run(self):
        build_py.run(self)
        # Copy version.json to the build directory
        if not self.dry_run:
            src = os.path.join(os.path.dirname(__file__), 'version.json')
            dst = os.path.join(self.build_lib, 'version.json')
            if os.path.exists(src):
                self.mkpath(os.path.dirname(dst))
                shutil.copy2(src, dst)

setup(
    py_modules=['main', 'version_manager'],
    cmdclass={'build_py': CustomBuildPy},
)
