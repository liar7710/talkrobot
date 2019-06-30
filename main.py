from tkinter import scrolledtext,Tk,Button,X,END,Frame
from lib.audio import *
from lib.AI import *
import time,os,webbrowser
class Turing:
    def __init__(self,APP_ID,API_KEY,SECRET_KEY,locpla):
        self.baiduai=BaiduRest(APP_ID,API_KEY,SECRET_KEY,locpla)
        self.audio=wave_file(locpla)

    def sendmessage(self,name,msg):
        msgcontent = name + ':' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n '
        text_msglist.insert(END, msgcontent, 'green')
        text_msglist.insert(END, msg)

    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def post(self):
        login_data = parse.urlencode([
        ("key","7bd84242739f4028aba2acdc0a46675a"),
        ("info",text_msg.get('0.0', END)),
        ("loc", '河南省南阳市宛城区南阳理工学院'),
        ("lon", '112.550190'),
        ("lat", '32.971450'),
        ("userid","122620")
        ])
        self.sendmessage('我',text_msg.get('0.0', END))
        text_msg.delete('0.0', END)
        with urlopen(Request('http://www.tuling123.com/openapi/api'), data=login_data.encode('utf-8')) as f:
            d=json.loads(f.read())
            if str(d['code'])=="100000":
                ans=d['text']+'\n'
                self.sendmessage('图灵',ans)
                self.baiduai.getVoice(d['text'],'turing.mp3')
            if str(d['code'])=="200000":
                ans=d['text']+'\n'+d['url']+'\n'
                webbrowser.open(d['url'])
                self.sendmessage('图灵',ans)
                self.baiduai.getVoice(d['text'], 'turing.mp3')
            elif str(d['code'])=="302000":
                for i in d['list']:
                    ans='标题:'+i['article']+'\n'+'来源:'+i['source']+'\n'+'图标:'+i['icon']+'\n'+'详细链接:'+i['detailurl']+'\n'
                    webbrowser.open(d['detailurl'])
                    self.sendmessage('图灵',ans)
                    self.baiduai.getVoice(ans,'turing.mp3')
            elif str(d['code'])=="308000":
                for i in d['list']:
                    ans='名称'+i['name']+'\n'+'图标'+i['icon']+'\n'+'信息'+i['info']+'\n'+'详情链接'+i['detailurl']+'\n'
                    webbrowser.open(d['detailurl'])
                    self.sendmessage('图灵',ans)
                    self.baiduai.getVoice(ans, 'turing.mp3')
        self.audio.play('turing.wav')

    def func(self):
        self.audio.my_record('user.wav')
        result = self.baiduai.getText('user.wav')
        text_msg.insert(END, result['result'])

APP_ID='10324119'
API_KEY='kSwNauMWCpMohwnXMOPwByGB'
SECRET_KEY ='EGFYc0gpoKF3lHnEGiMbrCG9ykgvp5HV'
locpla= os.path.abspath('.')+'\\'
f=Turing(APP_ID,API_KEY,SECRET_KEY,locpla)
root = Tk()
root.title('与图灵珩聊天中')
text_msglist=scrolledtext.ScrolledText(root)
text_msg=scrolledtext.ScrolledText(root,height=2)
button_sendmsg=Button(root, text='发送', command=f.post)
button_audio=Button(root, text='语音', command=f.func)
text_msglist.tag_config('green', foreground='#008B00')
text_msglist.pack(fill=X,expand=1)
text_msg.pack(fill=X,expand=1)
button_sendmsg.pack(fill=X,expand=1)
button_audio.pack(fill=X,expand=0.5)
root.mainloop()
