import speech_recognition as sr

listener = sr.Recognizer()
language = listener.__getattribute__

def listen():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Escuchando....")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice,language="es")
            rec = rec.lower()
            ##print(rec)
    except:
        rec = ""
    return rec