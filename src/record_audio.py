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
		self.stream = self.audio_instance.open(format=self.format, channels=self.channels, rate=self.rate,
		                                       input=True)

	# Record audio without a limit duration
	def record(self):
		while True:
			data = self.stream.read(self.chunk)
			self.frames.append(data)

			if self.pause:
				self.stop()

	# Stop recording
	def stop(self, path_audio_file):
		self.stream.stop_stream()
		self.stream.close()
		self.audio_instance.terminate()

		with wave.open("../audios/teste.wav", 'wb') as wf:
			wf.setnchannels(self.channels)
			wf.setsampwidth(self.audio_instance.get_sample_size(self.format))
			wf.setframerate(self.rate)
			wf.writeframes(b''.join(self.frames))

