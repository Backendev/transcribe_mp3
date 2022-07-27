from google.cloud import speech
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import mediainfo_json
from pydub.silence import detect_nonsilent
from scipy.io import wavfile 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os,glob
from textblob import TextBlob


class Utils:
    def __init__(self):
        self.ini = "1"
        self.actual_dir = os.getcwd()
        self.result = ""
        self.words = []

    def read_mp3(self,route,words):
        response = {}
        self.result = ""
        duration = 0
        temp_word_list = words.split(",")
        for word_temp_item in temp_word_list:
            self.words.append(word_temp_item.lower())
        words_match = {}
        destination_route = self.actual_dir+"/audio_convert/convert.wav"
        audSeg = AudioSegment.from_mp3(route)
        audSeg.export(destination_route, format="wav")
        song = AudioSegment.from_wav(destination_route) 
        r = sr.Recognizer() 
        chunks = split_on_silence(song, 
            min_silence_len = 1000,
            silence_thresh = -40
        )
        print(self.actual_dir)
        os.chdir('audio_chunks')
        i = 0
        for chunk in chunks:
            print("saving chunk{0}.wav".format(i))
            chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
            filename = 'chunk'+str(i)+'.wav'
            print("Processing chunk "+str(i))
            file = filename
            with sr.AudioFile(file) as source:
                audio_listened = r.listen(source) 
            try: 
                rec = r.recognize_google(audio_listened,language="en-US")
                self.result += str(rec)+" "
                list_w = rec.split(" ")
                list_w = [i.lower() for i in list_w]
                word_in_list = False
                steps_time = []
                complete = False
                init_temp = 0
                alternatives = {}
                for word in self.words:
                    if word.lower() in list_w:
                        if not word_in_list:
                            steps_time = self.extract_steps(os.getcwd()+"/"+file)
                            for j in range(0,len(steps_time) - 1):
                                alternative = []
                                if complete:
                                    init_temp = steps_time[j]
                                complete = False
                                temp_chunk = chunk[init_temp:steps_time[j+1]]
                                temp_chunk.export(f"./temp_chunk{i}_{j}.wav", bitrate ='192k', format ="wav") 
                                temp_filename = './temp_chunk'+str(i)+'_'+str(j)+'.wav'
                                with sr.AudioFile(temp_filename) as temp_source:
                                    audio_listened_temp = r.listen(temp_source)
                                try:
                                    rec_temp = r.recognize_google(audio_listened_temp,language="en-US",show_all=True)
                                    try:
                                        alternative = [value['transcript'] for value in rec_temp['alternative']]
                                    except:
                                        pass
                                    alternatives[str(init_temp)] = alternative
                                    if rec_temp != []: 
                                        complete = True
                                except sr.UnknownValueError:
                                    print("Could not understand audio") 
                                except sr.RequestError as e: 
                                    print("Could not request results. check your internet connection")
                            print(steps_time)
                            print(alternatives)
                            print(str(type(source)))
                            print(str(type(chunk)))
                        word_in_list = True
                        
                        result_times = self.times_in_results(steps_time,alternatives,list_w,duration)
                        
                        for item_list in range(0,len(list_w)):
                            low_word = list_w[item_list].lower()
                            if low_word in self.words:
                                if low_word in words_match:
                                    words_match[low_word]['count'] += 1
                                    words_match[low_word]['in_timeline'].append(result_times[item_list][list_w[item_list]])
                                else:
                                    words_match[low_word]={'count' : 1,'in_timeline':[result_times[item_list][list_w[item_list]]]}
                        print(f"Result tiomes {result_times}")
                info =  dict(mediainfo_json(file, read_ahead_limit=-1))
                duration = duration + int(float(info['streams'][0]['duration'])*1000)
            except sr.UnknownValueError: 
                print("Could not understand audio") 
            except sr.RequestError as e: 
                print("Could not request results. check your internet connection") 
            i += 1
        os.chdir('..')
        print(self.result)
        feel_analisis = self.feel_analisis(self.result)
        response['words_match'] = words_match
        response['transcript'] = self.result
        response['FeelAnalisis'] = feel_analisis
        data = {'mp3_file':route,'response':response}
        return response
    
    def extract_steps(self,audio_file): 
        audio = audio_file
        fs, Audiodata = wavfile.read(audio)
        AudiodataScaled = Audiodata/(2**15)
        timeValues = np.arange(0, len(AudiodataScaled), 1)/ fs 
        timeValues = timeValues * 1000 
        total = list(zip(timeValues.tolist(),AudiodataScaled.tolist()))
        df = pd.DataFrame.from_records(total,columns=['time','scala'])
        duration_audio = int(df.tail(1)['time'].values[0])
        df['mayor']= df['scala'].apply(lambda x: 1 if x > 0.05 else 0)
        df['time_round'] = df['time'].apply(lambda x: int(x))
        df['diference_mayor'] = df['mayor'].diff()
        df['diference_time'] = df['time_round'].diff()
        df_copy = df[(df['diference_mayor'] > 0)]
        df_copy['diference_time'] = df_copy['time_round'].diff()
        df_copy_2 = df_copy[(df_copy['diference_time'] > 50)]
        list_steps = df_copy_2['time_round']
        result_list = list_steps.tolist()
        result_list.append(duration_audio)
        result_list.insert(0,0)
        return result_list
    
    def times_in_results(self,times,alternatives,words,duration):
        temp_words = words
        actual = 0
        diference = 0
        match_alternative = False
        results = {}
        for item_time in times:
            actual += 1
            init = 0
            match_alternative = False
            if str(item_time) in alternatives.keys():
                for alternative in alternatives[str(item_time)]:
                    list_sp = alternative.split()
                    lon_list = len(list_sp)
                    time = str(item_time)
                    for init_time in range(init,len(temp_words)):
                        list_search = temp_words[init_time:init_time+lon_list]
                        search = " ".join(list_search)
                        if alternative.lower() == search.lower():
                            temp_words = temp_words[init_time+lon_list::]
                            match_alternative = True
                            diference = diference + (init_time + lon_list)
                            item = diference - lon_list
                            item_long = item + (lon_list)
                            if item_long == item:
                                results[item] = actual -1
                            else:
                                for items in range(item,item_long):
                                    results[items] = actual -1
                            break
                    if match_alternative:
                        break
        result_fin = {}
        prev_time = 0
        for item_word in range(0,len(words)):
            if item_word in results.keys():
                result_fin[item_word] = {words[item_word]:times[results[item_word]]+duration}
                prev_time = results[item_word]
            else:
                result_fin[item_word] = {words[item_word]:times[prev_time + 1]+duration}
        return result_fin

    def feel_analisis(self,text):
        analisisPol = TextBlob(text).polarity
        analisisSub = TextBlob(text).subjectivity
        feel = ""
        percent = 0
        subjetive = ""
        if analisisPol < 0:
            feel = "Negative"
            percent = int(abs(analisisPol) * 100)
        if analisisPol == 0:
            feel = "Neutral"
            percent = 100
        if analisisPol > 0:
            feel = "Positive"
            percent = int(analisisPol * 100)
        if analisisSub < 0:
            subjetive = "Objetive"
            subjetive_percent = int(abs(analisisSub) *100)
        if analisisSub == 0:
            subjetive = "Neutral"
            subjetive_percent = 100 
        if analisisSub > 0:
            subjetive = "Subjetive"
            subjetive_percent = int(analisisSub *100)
        return {"Polarity": f"{str(feel)} - {str(percent)}%","Subjective":f"{subjetive} - {str(subjetive_percent)}%" }
        


        
