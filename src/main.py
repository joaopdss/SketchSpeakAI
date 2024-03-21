import time
from record_audio import Audio
from cam_painter import Drawing
from gpt import OpenAI
from ppt import PowerPoint
import threading
import re

path_audio_file = "../audios/teste.wav"
recording_stats = False

# instantiate all the classes from files we need
audio_instance = Audio()
drawing_instance = Drawing()
openai_instance = OpenAI()
pptx_instance = PowerPoint()

# starting thread that will take care of the drawing window
threading.Thread(target=drawing_instance.start, daemon=True).start()

while True:

	# verify if the person clicked in the record button
	if drawing_instance.recording and not recording_stats:
		recording_stats = True
		# record audio
		recording_thread = threading.Thread(target=audio_instance.record, daemon=True, args=(path_audio_file,))
		recording_thread.start()
		# update status in the visual window
		drawing_instance.status = "Recording audio"
	elif not drawing_instance.recording and recording_stats:
		recording_stats = False
		audio_instance.pause = True
		# stop recording thread
		recording_thread.join()
		# save img canvas
		drawing_instance.save_img_canvas("../images/drawing.jpg")
		# get transcript of audio
		transcript = openai_instance.get_response(True, path_audio_file)
		# get summary of transcript
		summary = openai_instance.get_response(False, prompt=transcript)

		# process the summary to use later to create slide
		lines = summary.strip().split('\n')
		title = lines[0].replace('Title: ', '')
		summary = '\n'.join(lines[1:])
		summary = re.findall(r"\d+\.\s*(.*)", summary)
		summary = [topic for topic in summary if topic]

		# create pptx slide
		pptx_instance.create_pptx_slide(title, summary, "../images/drawing.jpg", "../presentations/teste.pptx")
		drawing_instance.status = "Slide created"

	# sleep to not use cpu all the time
	time.sleep(1)