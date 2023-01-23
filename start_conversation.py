#!/usr/bin/env python3

'''
    Speak with ChatGPT!

    Dependencies:
        - openai
        - SpeechRecognition
        - pyaudio
        - pyttsx3
'''

import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "YOUR_OPENAI_API_KEY"
MODEL_ENGINE = "text-davinci-003"
USER = "USER"
AI = "ChatGPT"


class SpeakAI(object):
    def __init__(self):
        self.r = sr.Recognizer()

    # given text, read it out loud using Google Assistant.
    # Return if the user still wants to continue the conversation
    def speak_text(self,
                   text,
                   conversation_history):
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            return False
        return True

    def get_response(self, prompt):
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

    def get_conversation(self,
                         conversation_history,
                         AI,
                         n=10):

        # if conversation is too long, take the last n prompts to be provided as history to the AI agent
        conv_len = len(conversation_history.split("::"))
        if conv_len > n:
            conversation_history = "::".join(
                conversation_history.split("::")[-(n):])

        response = self.get_response(conversation_history)

        # label response as the AI response. To be appended to conversation history
        response = response.split("::", 1)[1] if "::" in response else response
        conversation_history += "{0}:: {1} ".format(
            AI, response)

        return conversation_history, response

    def run(self):
        conversation_history = ""   # start a new conversation
        while True:
            try:
                with sr.Microphone() as source:

                    print("{0}: (Ask anything from ChatGPT ...)".format(USER))
                    # listen for USER input
                    audio = self.r.listen(source)

                    # Using Google Assistant to recognize audio
                    inputText = self.r.recognize_google(audio)
                    inputText = inputText.lower()
                    conversation_history += "USER:: {0}. ".format(inputText)

                    conversation_history, chatGPT_response = self.get_conversation(
                        conversation_history, AI, n=10)

                    print("{0}: {1} ".format(AI, chatGPT_response))
                    try:
                        continue_conversation = self.speak_text(chatGPT_response.split(
                            "::", 1)[1], conversation_history)
                    except:
                        continue_conversation = self.speak_text(
                            chatGPT_response, conversation_history)

                    if not continue_conversation:
                        print(
                            "\n\n #### Program terminated. Please find the transcript below. ####\n")
                        print(conversation_history)
                        break

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred!")

            except KeyboardInterrupt:
                print(
                    "\n\n #### Program terminated. Please find the transcript below. ####\n")
                print(conversation_history)
                break


if __name__ == "__main__":
    AI_agent = SpeakAI()
    AI_agent.run()
