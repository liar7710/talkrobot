from urllib.request import Request,urlopen
import json,base64
from urllib import parse
from pydub.audio_segment import AudioSegment
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert,locpla):
        # token认证的url
        self.locpla =locpla
        self.token_url = r'https://aip.baidubce.com/oauth/2.0/token'
        # 语音合成的resturl
        self.getvoice_url = r'http://tsn.baidu.com/text2audio'
        # 语音识别的resturl
        self.upvoice_url = r'http://vop.baidu.com/server_api'
        self.cu_id = cu_id
        self.getToken(api_key, api_secert)

    def getToken(self, api_key, api_secert):
        # 1.获取token
        data=parse.urlencode([
            ('grant_type','client_credentials'),
            ('client_id',api_key),
            ('client_secret',api_secert)
            ])
        f=urlopen(Request(self.token_url),data=data.encode('utf-8'))
        Token=json.loads(f.read())
        self.token_str = Token['access_token']
        f.close()

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        data=parse.urlencode([
            ('tex',text),
            ('lan','zh'),
            ('cuid',self.cu_id),
            ('ctp',1),
            ('tok',self.token_str)
        ])
        f=urlopen(Request(self.getvoice_url),data = data.encode('utf-8'))
        voice_fp = open(self.locpla+filename,'wb')
        voice_fp.write(f.read())
        voice_fp.close()
        f.close()
        sound = AudioSegment.from_mp3(self.locpla + "turing.mp3")
        sound.export(self.locpla + 'turing.wav', format="wav")
    def getText(self, filename):
        # 2. 向Rest接口提交数据
        data = {"format":"wav","rate":8000, "channel":1,"token":self.token_str,"cuid":self.cu_id,"lan":"zh"}
        # 语音的一些参数
        wav_fp = open(self.locpla+filename,'rb')
        voice_data = wav_fp.read()
        wav_fp.close()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data)
        r=urlopen(Request(self.upvoice_url),data=bytes(post_data,encoding="utf-8"))
        # 3.处理返回数据
        return json.loads(r.read())
