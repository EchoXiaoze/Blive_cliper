from pathlib import Path
import asyncio,threading

from bin.rec_live import recing_live,sync
from bin.const import Dirs
from bin.danmuku import Get_danmu
from bin.utils import prepare_environment


WORKING_DIR=Path(__file__).absolute().parent


# uid='2332440'  #主播的uid,输入主播uid会自动查找主播的房间号。
# clipman_list=['EchoXiaoze'] #程序听谁的弹幕指令


prepare_environment(WORKING_DIR) 
rec_save_path = WORKING_DIR / Dirs.records.value #录播文件夹
uid = ''
clipman_list = ['']


def Get_stream(uid,rec_save_path):
    sync(recing_live(uid,rec_save_path))


def thread_start():
    t1=threading.Thread(target=Get_danmu,args=(uid,clipman_list,WORKING_DIR,))
    t2=threading.Thread(target=Get_stream,args=(uid,rec_save_path,))

    t1.start()
    t2.start()
    
    t1.join()
    t2.start()


if __name__ == '__main__':
    print("预读取: " + uid + " ,切片MAN: " + clipman_list[0])
    if uid != '' or clipman_list[0] != '':
        thread_start()
    else:
        uid = input("请输入主播的UID号！(不是直播间号！！: ")
        clipman_list = input('请输入切片man的id！多个请用空格隔开: ').split(" ")
        thread_start()
