import speech_recognition as sr
import pyttsx3


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Распознавание...")
        command = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Вы сказали: {command}")
        return command
    except sr.UnknownValueError:
        print("Речь не распознана")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка при запросе к сервису распознавания: {e}")
        return ""


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def assistant():
    speak("Привет! Я ваш голосовой ассистент. Как я могу помочь вам сегодня?")

    while True:
        command = listen()

        if "пока" in command:
            speak("До свидания!")
            break
        elif "как дела" in command:
            speak("У меня всё отлично, спасибо!")
        else:
            speak("Извините, я не могу выполнить эту команду. Пожалуйста, повторите.")


if __name__ == "__main__":
    assistant()