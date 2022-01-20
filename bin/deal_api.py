from enum import Enum
from api_get import Get_api
from utils import check_floder
from pathlib import Path
WORKING_DIR = Path.cwd()

print(Get_api(uid="3723075")['liver_name'])
Api=Get_api(uid="3723075")
live_room=Api['live_room']
live_title=Api['live_title']
liver_name=Api['liver_name']
check_floder(path=WORKING_DIR / Path(f"{liver_name}-{live_room}"))
print(WORKING_DIR / Path(f"{liver_name}-{live_room}"))