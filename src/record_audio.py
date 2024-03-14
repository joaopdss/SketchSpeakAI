import pyaudio
import wave

class Audio:
	# Controls the audio recording

	def __init__(self):
		self.format = pyaudio.paInt16
		self.channels = 1
		self.rate = 44100
		self.chunk = 1024
		self.audio_instance = pyaudio.PyAudio()
		self.frames = []
		self.pause = False

	# Record audio without a limit duration
	def record(self):
		while True:
			data = self.stream.read(self.chunk)
			self.frames.append(data)

			if self.pause:
				self.stop()

	# Stop recording
	def stop(self):
		self.stream.stop_stream()
		self.stream.close()
		self.audio.terminate()

		with wave.open("../audios/teste.wav", 'wb') as wf:
			wf.setnchannels(self.channels)
			wf.setsampwidth(self.audio.get_sample_size(format))
			wf.setframerate(self.rate)
			wf.writeframes(b''.join(self.frames))

