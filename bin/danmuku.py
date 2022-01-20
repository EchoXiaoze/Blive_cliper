import secrets,time,re,subprocess,asyncio
from typing import List, Tuple
from pathlib import Path
from typing import Tuple
from bilibili_api import live, sync
from .api_get import Get_api
from .const import Dirs


# Tuple=[]
接收到的弹幕指令={
    '开切时间':'00:00:00',
    '结束时间':'00:00:00',
    '文件名':'',

}



def Get_danmu(uid,clipman_list,WORKING_DIR):
    开播时间=(int(time.time()))
    Api=Get_api(uid)
    live_room=Api['live_room']
    live_title=Api['live_title']
    liver_name=Api['liver_name']
    live_name=f"{live_room}-{liver_name}"
    room = live.LiveDanmaku(live_room)
    
    @room.on('DANMU_MSG')
    async def on_danmaku(event):
        # 收到弹幕
        comment = event['data']['info'][1]
        send_user = event['data']['info'][2][1]
        ts=event['data']['info'][9]['ts']
        print(f"[{unix_convert(ts,flag=0)}]'{send_user}' : '{comment}'")
        处理弹幕(clipman_list,comment,send_user,ts,开播时间,WORKING_DIR,live_name)
        
    sync(room.connect())



def unix_convert(ts,flag=1):
    '''
    flag为1的时候是发回字符串
    默认：flag为0返回字典
    '''
    Time_List={
        'Hour':'',
        'Min':'',
        'Sec':'',
    }
    Time=time.strftime("%H:%M:%S",time.localtime(ts))
    Time_List['Hour']=Time[:2]
    Time_List['Min']=Time[3:5]
    Time_List['Sec']=Time[6:8]
    if flag:
        return Time_List
    else:
        return f"{Time_List['Hour']}:{Time_List['Min']}:{Time_List['Sec']}"
    

def _convert_time(sec: int) -> str:
        hour = sec // 3600
        sec = sec % 3600
        minute = sec // 60
        sec = sec % 60
        return f"{hour:02}:{minute:02}:{sec:02}"


def 处理弹幕(clipman_list,comment,send_user,ts:int,开播时间,WORKING_DIR,live_name):
    # regex = r"@(开切|结束)(?:\s+|，|,)(\d+)(?:(?:，|,|\s*)(\w+))?"
    # match = re.match(regex,comment)
    if 匹配结果 := 解析弹幕指令(comment):
        操作, 偏移量, 标题 = 匹配结果
        # print( 操作, 偏移量, 标题)
    
    
        if send_user in clipman_list:
            if 操作 == '开切':
                接收到的弹幕指令['开切时间']=_convert_time(sec=(ts-开播时间-int(偏移量)))
            elif 操作 == '结束':
                接收到的弹幕指令['结束时间']=_convert_time(sec=(ts-开播时间+int(偏移量)))
                接收到的弹幕指令['文件名']=标题
                make_clips(WORKING_DIR,live_name)

def 解析弹幕指令(弹幕指令: str) -> Tuple[str, int, str]:
    分隔符 = [" ", "，", ","]
    分割符正则 = f'(?:{"|".join(分隔符)})'
    弹幕指令正则表达式 = rf"@(开切|结束){分割符正则}(-?\d+)(?:{分割符正则}(.+))?"
    if not (匹配结果 := re.match(弹幕指令正则表达式, 弹幕指令)):
        return None
    操作, 偏移量, 标题 = 匹配结果.groups()
    偏移量 = int(偏移量)
    print(操作, 偏移量, 标题)
    return (操作, 偏移量, 标题)


def check_danmu(comment):#匹配开始弹幕
    regex = r"'@(开切)(?:,|，|\s)(\d+)'"
    match = re.match(regex,comment)
    if match:
        return True
    else:
        return False


def make_clips(WORKING_PATH,live_name:Path):
    rec_path = WORKING_PATH / Dirs.records.value / live_name
    # print(rec_path)
    for file in rec_path.iterdir():
        rec_file = file
        '''
        这里可能会出现一个问题
        如果运行过程中，突然出现一个以上的文件，将会出现问题
        最好的解决方案是在生成直播文件后可以全局使用，但是我不知道如何从rec_live里的rec_file变量传过来
        '''
    clip_path = WORKING_PATH / Dirs.clips.value
    ffmpeg_path = WORKING_PATH / Path("bin/ffmpeg.exe")
    cmd = [
                ffmpeg_path,
                "-i",
                rec_file,  # 输入视频
                "-vcodec",
                "copy",
                "-acodec",
                "copy",
                "-ss",
                接收到的弹幕指令['开切时间'],  # 开始时间
                "-to",
                接收到的弹幕指令['结束时间'],  # 结束时间
                clip_path / Path(f"{接收到的弹幕指令['文件名']}.mp4"),  # 输出文件路径
                "-y",
            ]
    subprocess.run(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
    
