import openai
import os

openai.api_key = "xxxxxxxxxxxxx"

client = openai.OpenAI()

def get_response(audio, prompt=None, model="gpt-3.5-turbo-0125"):

	if audio:
		transcription = client.audio.transcriptions.create(
			model="whisper-1",
			file=audio_file
		)

		return transcription.text

	else:
		message = prompt

		resume = openai.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=message
		)

		return resume.choices

prompt = "Hey, give me some ideas for my new computer vision project!"

response = get_response(prompt)

print(response)