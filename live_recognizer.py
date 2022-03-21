import argparse
import math
import speech_recognition as sr
import os
import sys
from time import sleep

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer


client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

# initialize the recognizer
r = sr.Recognizer()
m = sr.Microphone()

keyword = "noordzee"
keyword2 = "zee"

def startListening(unused_addr, args, value):
	try:
		print("[{0}] ~ {1}".format(args[0], value))
		with m as source: audio_data = r.listen(source, phrase_time_limit=3)
		print("# SENDING TO GOOGLE FOR RECOGNITION #")
		text = r.recognize_google(audio_data, language="nl-NL")
		print(text)
		if (keyword.lower() in text.lower()) or (keyword2.lower() in text.lower()) :
			print("# KEYWORD DETECTED, LISTENING FOR TEXT #")
			client.send_message("/keywordDetected", 1)
			listenToQuestion()
		else:
			print("# NO KEYWORD DETECTED #")
			client.send_message("/keywordDetected", 0)
	except ValueError: pass

	except sr.UnknownValueError:
		print("# NO KEYWORD DETECTED #")
		client.send_message("/keywordDetected", 0)
	except sr.RequestError as e:
		print("#!#! ERROR FROM GOOGLE #!#!; {0}".format(e))
		client.send_message("/keywordDetected", 0)	

def listenToQuestion():
	print("# STARTING TO LISTEN TO SENTENCE #")
	with m as source: audio_data = r.listen(source, phrase_time_limit=20)
	try:
		text = r.recognize_google(audio_data, language="nl-NL")
		client.send_message("/detectedPhrase", 1)
		print("# TEXT DETECTED! #")
		print("{}".format(text))
		client.send_message("/phrase", text)
		print("# ANALYSIS OF SENTIMENT (POLARITY & SUBJECTIVITY) #")
		blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
		print("{}".format(blob.sentiment))
		client.send_message("/polarity", blob.sentiment[0])
		client.send_message("/subjectivity", blob.sentiment[1])

	except sr.UnknownValueError:
		client.send_message("/detectedPhrase", 0)
		print("# UNKNOWN VALUE - TRYING AGAIN #")
		sleep(0.1)
		listenToQuestion()
	except sr.RequestError as e:
		print("#!#! ERROR FROM GOOGLE #!#!; {0}".format(e))
		client.send_message("/detectedPhrase", 0)
	except ValueError: pass

if __name__ == "__main__":


	parser = argparse.ArgumentParser()
	parser.add_argument("--ip",
		default="127.0.0.1", help="The ip to listen on")
	parser.add_argument("--port",
		type=int, default=5006, help="The port to listen on")
	args = parser.parse_args()

	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/startListening", startListening, "Start Listening")

		# Print mic
	print(m.list_microphone_names())


	for i, microphone_name in enumerate(m.list_microphone_names()):
	    if microphone_name == "Microphone (3- USB Audio CODEC ": # SET RIGHT MIC HERE
	        m = sr.Microphone(device_index=i)
	        print("# RIGHT MIC FOUND!")

	client.send_message("/operation", 1)
	client.send_message("/keywordDetected", 0)
	print("# CALIBRATING... #")
	with m as source: r.adjust_for_ambient_noise(source, duration = 1)
	print("# MINIMUM SOUND LEVEL CALIBRATED AT {} #".format(r.energy_threshold))

	server = osc_server.ThreadingOSCUDPServer(
		(args.ip, args.port), dispatcher)
	print("Serving on {}".format(server.server_address))
	server.serve_forever()
  
  