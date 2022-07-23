from google.cloud import speech
import speech_recognition as sr
from pydub import AudioSegment
from pydub import AudioSegment 
from pydub.silence import split_on_silence
import os
class Utils:
    def __init__(self):
        self.ini = "1"
        self.actual_dir = os.getcwd()
        self.result = ""

    def read_mp3(self,route):
        route = self.actual_dir+"/examples/"+route
        origin_audio = route
        destination_route = self.actual_dir+"/audio_convert/convert.wav"
        audSeg = AudioSegment.from_mp3(route)
        audSeg.export(destination_route, format="wav")
        recognizer = sr.Recognizer()
        # with sr.AudioFile(destination_route) as source:
        #     recorded_audio = recognizer.listen(source)
        #     print("Done recording")
        # try:
        #     print("Recognizing the text")
        #     text = recognizer.recognize_google(
        #             recorded_audio, 
        #             language="en-US"
        #         )
        #     print("Decoded Text : {}".format(text))

        # except Exception as ex:
        #     print(ex)
        song = AudioSegment.from_wav(destination_route) 
        chunks = split_on_silence(song, 
            min_silence_len = 500, 
            silence_thresh = -40
        ) 
        os.chdir('audio_chunks')
        i = 0
        for chunk in chunks:
            print("saving chunk{0}.wav".format(i))
            chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
            filename = 'chunk'+str(i)+'.wav'
            print("Processing chunk "+str(i)) 
            file = filename 
            r = sr.Recognizer() 
            with sr.AudioFile(file) as source:
                audio_listened = r.listen(source) 
            try: 
                rec = r.recognize_google(audio_listened,language="en-US") 
                print(f"rec  -- {rec}")
            except sr.UnknownValueError: 
                print("Could not understand audio") 
            except sr.RequestError as e: 
                print("Could not request results. check your internet connection") 
            i += 1
        os.chdir('..') 
        
