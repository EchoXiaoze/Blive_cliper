import os,sys
from pathlib import Path
from tkinter import W



WORKING_DIR = Path(__file__).absolute().parent
requirements = WORKING_DIR / Path("requirements.txt")
README = WORKING_DIR / Path("README.txt")


os.popen(f"pip install -r {requirements} -i https://pypi.mirrors.ustc.edu.cn/simple/",mode=W)
os.popen(f"start {README}")