import cv2

from record_audio import Audio
from cam_painter import Drawing
from gpt import OpenAI
from ppt import PowerPoint
import threading
import re

path_audio_file = "../audios/teste.wav"
recording_stats = False
audio_instance = Audio()
drawing_instance = Drawing()
openai_instance = OpenAI()
pptx_instance = PowerPoint()

threading.Thread(target=drawing_instance.start, daemon=True).start()

while True:

	if drawing_instance.recording and not recording_stats:
		recording_stats = True
		recording_thread = threading.Thread(target=audio_instance.record, daemon=True, args=(path_audio_file,))
		recording_thread.start()
	elif not drawing_instance.recording and recording_stats:
		recording_stats = False
		audio_instance.pause = True
		recording_thread.join()
		drawing_instance.save_img_canvas("../images/drawing.jpg")

		transcript = openai_instance.get_response(True, path_audio_file)
		summary = openai_instance.get_response(False, prompt=transcript)

		lines = summary.strip().split('\n')
		title = lines[0].replace('Title: ', '')
		summary = '\n'.join(lines[1:])
		summary = re.findall(r"\d+\.\s*(.*)", summary)
		summary = [topic for topic in summary if topic]

		pptx_instance.create_pptx_slide(title, summary, "../images/drawing.jpg", "../presentations/teste.pptx")
		print("Slide created")