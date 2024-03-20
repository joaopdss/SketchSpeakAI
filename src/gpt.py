import openai

class OpenAI:

	def __init__(self):
		openai.api_key = "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"
		self.client = openai.OpenAI(api_key="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")

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
			prompt = f"I want you to summarize in three small topics what was said in this content and give a title for it, no yapping: {prompt}"

			response = openai.chat.completions.create(
				model="gpt-3.5-turbo",
				messages= [{"role": "system", "content": "Always translate your response to English language"}, {"role": "user", "content": prompt}]
			)
			print(response)
			response = response.choices[0].message.content

		return response

