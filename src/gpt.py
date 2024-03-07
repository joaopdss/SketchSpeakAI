import openai

class OpenAI:

	def __init__(self):
		self.client = openai.OpenAI(api_key="xxxxxxxxx")

	# get response from gpt, can send an audio if audio=True to return the transcription or another thing by sending a text
	def get_response(self, is_audio, audio_file=None, prompt=None):

		if is_audio:
			audio_file = open(audio_file, "rb")

			response = self.client.audio.transcriptions.create(
				model="whisper-1",
				file=audio_file,
				response_format="text"
			)

		else:

			response = openai.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=prompt
			)

			response = response.choices

		return response

