# Speak with ChatGPT

A simple Python-only tool to have a voice conversation with ChatGPT. This involves your voice recognition (voice-to-text) and converting ChatGPT response to voice (text-to-voice) output using Google Assistant. Modifications and improvements to the code are welcome.

## Installation

`pip install -r requirements.txt`

Note that installing `pyaudio` using `pip` may produce errors. In this case, please follow these stack overflow threads ([Ubuntu](https://stackoverflow.com/questions/48690984/portaudio-h-no-such-file-or-directory), [Mac](https://stackoverflow.com/questions/33851379/how-to-install-pyaudio-on-mac-using-python-3)).

## Usage

Obtain your OpenAI API Key from OpenAI [website](https://beta.openai.com/account/api-keys). Then add this key to `start_conversation.py` (line 17).

You may now start a voice conversation with ChatGPT.

```
python start_conversation.py
```
