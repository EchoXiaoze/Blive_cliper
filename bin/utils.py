from .const import Dirs
from pathlib import Path
from .api_get import Get_api

WORKING_DIR = Path(__file__).absolute().parent.parent
print(WORKING_DIR)
def prepare_environment(working_dir):
    # print(WORKING_DIR)
    for dir in Dirs:
        dir: Path = working_dir / dir.value
        if not dir.exists():
            dir.mkdir()
    
    check_bin(WORKING_DIR / Path("bin"))
    


def check_bin(bin_path: Path):
    if not bin_path.exists():
        raise FileNotFoundError(bin)
    return True


def check_floder(path: Path):
    if not path.exists():
        path.mkdir()
    return True


def existence(path=Path):   #判断文件夹是否为空
    '''
    如果为空返回True，反之False
    '''
    for x in path.parent.iterdir():
        if x.is_dir():
            if x == path:
                flag = False
                for j in x.iterdir():
                    flag = True
                    break
                if flag :
                    return False
                else:
                    return True




'''
1.判断有没有这个主播的文件夹，没有则创建，并在内创建往期录播

2.判断这个主播的文件夹里有没有东西，如果有，把文件移入往期录播

'''

def check_live_folder(path=Path):
    '''
    path=参数最好在Path(里面加路径，如下)
    p=Path(f"{path}\\{live_room}-{liver_name}")
    有对应文件夹则不创建，反之则创建
    '''
    if not path.exists():
        path.mkdir()
    else:
        for x in path.parent.iterdir():
            if x.is_dir():
                if x == path:#这个主播文件夹存在
                    if existence(path=path):#里面没有文件
                        break
                    else:
                        '''删掉主播文件夹里的录播'''
                        for i in path.iterdir():
                            print(f'''
[For_Rina][警告]: 已将 “{i.name}”移动到【往期录播】文件夹中...
''')
                            # i.unlink(WORKING_DIR / Dirs.former_rec.value)
                            # print(WORKING_DIR / Dirs.former_rec.value /Path(i.name))
                            i.replace(WORKING_DIR / Dirs.former_rec.value /Path(i.name))
                        break






    




# path = str(WORKING_DIR / Dirs.records.value)
# uid="3723075"
# Api=Get_api(uid)
# live_room=Api['live_room']
# live_title=Api['live_title']
# liver_name=Api['liver_name']

# check_live_folder(path=Path(f"{path}\\{live_room}-{liver_name}"))