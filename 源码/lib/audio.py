import wave
from pyaudio import PyAudio,paInt16
class wave_file:
    def __init__(self,locpla,framerate=8000,NUM_SAMPLES=2000,channels=1,sampwidth=2,TIME=2,chunk=2014):
        self.framerate = 8000
        self.NUM_SAMPLES = 2000
        self.channels = 1
        self.sampwidth = 2
        self.TIME = 5
        self.chunk = 2014
        self.locpla=locpla

    def save_wave_file(self,filename,data):
        wf=wave.open(self.locpla+filename,'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def my_record(self,filename):
        pa=PyAudio()
        stream=pa.open(format = paInt16,channels=1,rate= self.framerate,input=True,frames_per_buffer= self.NUM_SAMPLES)
        my_buf=[]
        count=0
        while count< self.TIME*4:#控制录音时间
            string_audio_data = stream.read( self.NUM_SAMPLES)
            my_buf.append(string_audio_data)
            count+=1
        self.save_wave_file(filename,my_buf)
        stream.close()
    def play(self,filename):
        #os.popen(self.locpla+filename )
        wf=wave.open(self.locpla+filename,'rb')
        p=PyAudio()
        stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
        data = wf.readframes(self.chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(self.chunk)
        stream.close()
        p.terminate()

