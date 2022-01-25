import requests;
import time;
import pyautogui;

class Danmu():
    def __init__(self):
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory';
        # 请求头
        self.headers = {
            'Host':'api.live.bilibili.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
        # 定义POST传递的参数
        self.data = {
            # 直播间ID
            'roomid':'23055314',
            'csrf_token':'',
            'csrf':'',
            'visit_id':'',
        }
        # 日志写对象
        self.log_file_write = open('danmu.log',mode='a',encoding='UTF-8');
        # 读取日志
        log_file_read = open('danmu.log',mode='r',encoding='UTF-8');
        self.log = log_file_read.readlines();
        
    def get_danmu(self):
        # 获取直播间弹幕
        html = requests.post(url=self.url,headers=self.headers,data=self.data).json();
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname'];
            # 获取发言
            text = content['text'];
            # 获取发言时间
            timeline = content['timeline'];
            # 拼接 时间 昵称 弹幕 记录发言
            msg = timeline+' '+nickname+': '+text;
            # 判断对应消息是否存在于日志，如果和最后一条相同则打印并保存
            if msg+'\n' not in self.log:
                # 打印消息(发的弹幕信息)
                print(msg)
                # 保存日志
                self.log_file_write.write(msg+'\n');
                # 添加到日志列表
                self.log.append(msg+'\n');
                # 判断text中是否只有数字和空格
                to_my_linking = lambda x: all(var.isdigit() for var in x.split())
                if to_my_linking(text) == True:
                    # 如果只有数字和空格 拆成三分
                    cmd = text.split()
                    x = int(cmd[0])
                    y = int(cmd[1])
                    z = int(cmd[2])
                    # 高级扫雷宽度30 高度16 有三种鼠标操作
                    if x<=30 and y<=16 and z<=3:
                        # 扫雷界面宽度1000px
                        pyautogui.moveTo(68 + (30 * (x-1)),128 + (30 * (y-1)))
                        if z == 1:
                            pyautogui.click()
                        if z == 2:
                            pyautogui.rightClick()
                        if z == 3:
                            pyautogui.middleClick()
                # 扫雷失败了按P键重开
                if text == 'restart':
                    pyautogui.press('p')
            # 清空变量缓存
            nickname = '';
            text = '';
            timeline = '';
            msg = '';
# 创建bDanmu实例
bDanmu = Danmu();
while True:
    # 暂停0.5防止cpu占用过高
    time.sleep(0.5);
    # 获取弹幕
    bDanmu.get_danmu();  