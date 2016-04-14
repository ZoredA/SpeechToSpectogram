# This file is in charge of the speech recognition work.

# Uses the speech recognition library: https://pypi.python.org/pypi/SpeechRecognition/
from os import path
import speech_recognition as sr

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "tmp/output.wav")

def recognize_file(audio_file):
    r = sr.Recognizer()
    #r.energy_threshold = 4000
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    likely_text = r.recognize_google(audio, show_all=True)
    return likely_text


if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))