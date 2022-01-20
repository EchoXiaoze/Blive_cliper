import requests

def Get_api(uid):
    '''
    uid->主播的uid，在用户空间查找

    live_room :"主播的直播房间号"
    live_title  :"主播的直播标题"
    live_status :"主播的直播状态" 0为未开播 1为直播中

    '''

    headers = {  # 请求的头部
        'origin': "https://space.bilibili.com",
        'referer': "https://space.bilibili.com/",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        'Host': "api.bilibili.com"
        }
    url='https://api.bilibili.com/x/space/acc/info?mid='+uid+'&jsonp=jsonp'
    res = requests.get(url,headers=headers)
    res_json=res.json()['data']['live_room']
    live_list = {'live_room':'',
                'live_title':'',
                'live_status':'',
                'liver_name':'',
                }
    live_list['live_room'] =  res_json['roomid']
    live_list['live_title'] =  res_json['title']
    live_list['live_status'] =  res_json['liveStatus']
    live_list['liver_name'] = res.json()['data']['name']
    return live_list








