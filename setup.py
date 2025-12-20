from setuptools import setup
from setuptools.command.install import install
import shutil
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        # Copy version.json to the same directory as the installed modules
        if self.install_lib:
            src = os.path.join(os.path.dirname(__file__), 'version.json')
            dst = os.path.join(self.install_lib, 'version.json')
            if os.path.exists(src):
                shutil.copy2(src, dst)

setup(
    py_modules=['main', 'version_manager'],
    cmdclass={'install': CustomInstall},
)
