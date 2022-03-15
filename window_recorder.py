import tkinter
import speech_recognition

window = tkinter.Tk()
window.geometry('650x450')
window.title("Запись с микрофона / Speech to text")
window.resizable(False, False)

# textarea
textarea = tkinter.Text(window)
textarea.place(x=0, y=0)

# Defaults values for elements (with state)
defaults = {
    "button": {
        "start": "Начать запись",
        "stop": "Остановить",
    },
    "label": {
        "wait": "Нажмите на кнопку и говорите",
        "listen": "Говорите...",
        "not_exceed": "Речь не понятна или не слышна... Повторите еще раз."
    }
}

recognizer = speech_recognition.Recognizer()


def speech():
    with speech_recognition.Microphone() as mic:
        recognize_text = ''

        # Button pressed and mic listen
        txt_label.configure(text=defaults["label"]["listen"])
        button_rec.configure(text=defaults["button"]["stop"])
        window.update()

        try:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic, timeout=7, phrase_time_limit=10)
            recognize_text = recognizer.recognize_google(audio, language='ru-RU')

        except (speech_recognition.WaitTimeoutError, speech_recognition.UnknownValueError):
            button_rec.configure(text=defaults["button"]["start"])
            txt_label.configure(text=defaults["label"]["not_exceed"])
            window.update()
            return

        else:
            # Reset state
            txt_label.configure(text=defaults["label"]["wait"])
            button_rec.configure(text=defaults["button"]["start"])

            return recognize_text.capitalize()


def insert_record():
    textarea.insert('end', speech() + '\n')


button_rec = tkinter.Button(window, text=defaults["button"]["start"], bg='red', font=('Arial', 16), command=insert_record)
button_rec.place(x=30, y=400)

txt_label = tkinter.Label(window, text=defaults["label"]["wait"], font=('Arial', 12))
txt_label.place(x=200, y=408)

window.mainloop()
