import time
from os import path
import speech_recognition as sr
import yaml
import urllib
import os
import re
import os
from gtts import gTTS
import pygame
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

r = sr.Recognizer()
__all__ = ['recognition.listening', 'recognition.match']
class recognition:
    def listening(self):
        text = "erreur"
        with sr.Microphone() as source:
            #cls()
            r.adjust_for_ambient_noise(source)
            #cls()
            audio = r.listen(source)
        try:
            text = r.recognize_wit(audio, key="KRBQCEKL3AJQBAKO6ZXIROQ7X4EAJ76L").lower()
        except sr.UnknownValueError:
            print("Impossible de comprendre")
        return text
    def match(self, a, b, c):
        with open(b, 'r') as recup:
            config1 = yaml.load(recup)
        for config2 in config1["configuration"]:
            answer = config2["answer"]
            cmd = config2["cmd"]
            phrase = config2["phrase"]
            if re.match(phrase , a):
                tts = gTTS(text=answer, lang=c)
                tts.save("answer.mp3")
                pygame.mixer.init()
                pygame.mixer.music.load("answer.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
                os.system(cmd)