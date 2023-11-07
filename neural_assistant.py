from neuralintents import BasicAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

speaker.say("Hello my friend")
speaker.runAndWait()


def create_note():
    global recognizer

    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    complete = False
    while not complete:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio_input = recognizer.listen(mic)

                note = recognizer.recognize_google(audio_input)
                note = note.lower()

                speaker.say("What should we name the file?")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio_input = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio_input)
                filename = filename.lower()

            with open(f"{filename}", 'w') as f:
                complete = True

                f.write(note)
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say("What todo do you want to add?")
    speaker.runAndWait()

    complete = False
    while not complete:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio_input = recognizer.listen(mic)

                item = recognizer.recognize_google(audio_input)
                item = item.lower()

                todo_list.append(item)
                complete = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()


def show_todos():
    speaker.say("The items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello. Hot can I do for you?")
    speaker.runAndWait()


def exit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit()


todo_list = ['Go shopping', 'Clean Room', 'Record Video']
mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": exit
}

assistant = BasicAssistant('intents.json', method_mappings=mappings)
assistant.fit_model(epochs=50)
assistant.save_model()

# Load saved models
# assistant.load_model(model_name='models/todos')

# Save models
# assistant.save_model(model_name='models/todos')

complete = False

while not complete:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio_input = recognizer.listen(mic)

            message = recognizer.recognize_google(audio_input)
            message = message.lower()

            if message == "stop":
                complete = True

        assistant.process_input(message)
        print(assistant.process_input(message))

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
