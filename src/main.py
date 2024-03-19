from record_audio import Audio
from cam_painter import Drawing
from gpt import OpenAI

path_audio_file = "../audios/teste.wav"
recording_stats = False
audio_instance = Audio()
drawing_instance = Drawing()
openai_instance = OpenAI()

drawing_instance.start()


while True:

	if drawing_instance.recording and not recording_stats:
		print("entrei")
		recording_stats = True
		audio_instance.record()
	elif not drawing_instance and recording_stats:
		print("Koeeeeeeeeeeeeeeeeeeeeeeee")
		recording_stats = False
		audio_instance.stop(path_audio_file)

		transcript = openai_instance.get_response(True, path_audio_file)
		resume = openai_instance.get_response(False, prompt=transcript)