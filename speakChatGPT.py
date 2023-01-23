#!/usr/bin/env python3

'''
    Speak with ChatGPT!

    Dependencies:
        - openai
        - SpeechRecognition
        - pyaudio
'''

import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "YOUR_OPENAI_API_KEY"
r = sr.Recognizer()
MODEL_ENGINE = "text-davinci-003"
USER = "USER"
AI = "ChatGPT"


# given text, read it out loud using Google Assistant
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_response(prompt):
    response = openai.Completion.create(
        model=MODEL_ENGINE,
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # return converted text
    return response.choices[0].text


def get_conversation_history(
        input_prompt,
        conversation_history,
        USER,
        AI,
        n=10):

    # if conversation is too long, take the last n prompts
    conv_len = len(conversation_history.split("\n"))
    if conv_len > n:
        conversation_history = ":".join(
            conversation_history.split("::")[-(n):])

    response = get_response(conversation_history)
    conversation_history += "{0}: {1}. ".format(
        AI, response)

    return conversation_history, response


def run():
    conversation_history = ""   # start a new conversation
    while True:
        try:
            with sr.Microphone() as source:
                # wait till the voice recogniser adjusts to the environment
                # r.adjust_for_ambient_noise(source, duration=0.2)

                print("\n{0}: (Ask anything from ChatGPT ...)".format(USER))
                # listens for the user's input
                audio = r.listen(source)

                # Using Google Assistant to recognize audio
                inputText = r.recognize_google(audio)
                inputText = inputText.lower()
                conversation_history += "USER:: {0}. ".format(inputText)

                conversation_history, chatGPT_response = get_conversation_history(
                    inputText, conversation_history, USER, AI, n=10)

                print("{0}: {1} ".format(AI, chatGPT_response))
                try:
                    speak_text(chatGPT_response.split("::", 1)[1])
                except:
                    speak_text(chatGPT_response)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")


if __name__ == "__main__":
    run()
