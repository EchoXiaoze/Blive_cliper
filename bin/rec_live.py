from bilibili_api import live, sync
import aiohttp
from pathlib import Path
import time


# from .const import Dirs
from .api_get import Get_api
from .utils import check_live_folder




async def recing_live(uid,rec_save_path):
    Api=Get_api(uid)
    time.sleep(0.1)
    live_room=Api['live_room']
    live_title=Api['live_title']
    liver_name=Api['liver_name']
    # 初始化
    room = live.LiveRoom(live_room)
    # 获取直播流链接
    stream_info = await room.get_room_play_url()
    url = stream_info['durl'][0]['url']
    localtime = time.strftime("%Y年%m月%d日%H点场",time.localtime())
    rec_file=Path(f"{rec_save_path}\{live_room}-{liver_name}\{liver_name}-{live_title}-{localtime}.flv")
    check_live_folder(path=Path(f"{rec_save_path}\\{live_room}-{liver_name}"))
    async with aiohttp.ClientSession() as sess:
        # 设置 UA 和 Referer 头以绕过验证
        async with sess.get(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com/"},timeout=0) as resp:
            # 以二进制追加方式打开文件以存储直播流
            flag=False
            with open(rec_file, 'ab') as f:
                while True:
                    # 循环读取最高不超过 1024B 的数据
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        # 无更多数据，退出循环
                        print('无更多数据')
                        break
                    # print(f'接收到数据 {len(chunk)}B')
                    if flag:
                        pass
                    else:
                        flag=True
                        print(f'[For_Rina][信息]: 正在下载[{live_room}]直播推流')
                    # 写入数据
                    f.write(chunk)

# sync(recing_live(uid=uid,rec_save_path=path))#path = str(WORKING_DIR / Dirs.records.value)
