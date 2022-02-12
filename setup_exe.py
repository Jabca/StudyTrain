from cx_Freeze import setup, Executable
import subprocess
import sys

version = "0.6"
"""PACKAGES = []
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
installed_packages = installed_packages.split('\r\n')
EXCLUDES = {pkg.split('==')[0] for pkg in installed_packages if pkg != ''}
EXCLUDES.remove("python-docx")
EXCLUDES.remove("Pillow")

for pkg in PACKAGES:
    if type(pkg) == str: EXCLUDES.remove(pkg)
    else: EXCLUDES.remove(pkg[1])
"""

build_exe_options = {
    "packages": ["tkinter", "docx", "PIL"],
    "include_files": ["gui/", "lib/"],
    "optimize": 2
}
bdist_msi_options = {
    'add_to_path': True,
}


base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("generate_tasks.py", base=base, targetName="task_generator.exe")]

setup(
    name="Cross Section task generator",
    version=version,
    description="App to generate task for students to practice",
    options={
        'bdist_msi': bdist_msi_options,
        'build_exe': build_exe_options},
    executables=executables,
)