# shitty script by SilentTem

import os
import platform
import inspect
import subprocess
import time
import configparser

config = configparser.ConfigParser()
config.read("spatial_audio_tools.ini")

config_drp_outputchannelcfg = config.get(
	"DRP Settings",
	"OutputChannelCfg",
	fallback="9.1.6"
)

config_ffmpeg_outputformat = config.get(
	"FFmpeg Settings",
	"OutputFormat",
	fallback="flac"
)

def clear_screen():
	if platform.system() == "Windows":
		os.system("cls")
	elif platform.system() == "Darwin" or platform.system() == "Linux":
		os.system("clear")
	else:
		print("Unknown OS, cannot clear screen")

def pause_and_wait():
	if platform.system() == "Windows":
		os.system("pause")
	#elif platform.system() == "Darwin" or platform.system() == "Linux":
	#	os.system("wait")
	else:
		input("Press Enter to continue...")

def create_dir(name):
	if not os.path.exists(name):
		os.mkdir(name)

def invoke_drp(args):
	global drp_process
	drp_process = subprocess.Popen(f"drp.exe {args}")

def invoke_ffmpeg(args):
	global ffmpeg_process
	ffmpeg_process = subprocess.Popen(f"ffmpeg.exe {args}")

while True:
	try:
		print(
			inspect.cleandoc("""
				Choose mode
				1. Convert Atmos to WAV
				2. Convert Atmos to WAV, then convert channels to multiple files (format can be configured in ini)
			""")
		)
		print()

		user_input_mode = int(input("Type a number: "))
		print()

		if user_input_mode < 1 or user_input_mode > 2:
			raise ValueError
		break
	except ValueError:
		print(f"Invalid character, must be within a range of 1-2")
		pause_and_wait()
		clear_screen()
		continue
	break

clear_screen()

print(f"User specified mode {user_input_mode}")
print()

file_list = []

directory = os.getcwd()
for filename in os.listdir(directory):
	supported_exts = (".m4a", ".mp4", ".ec3")
	if filename.endswith(supported_exts):
		with open(os.path.join(directory, filename)) as f:
			filename_fullpath = f.name
			filename_noext = filename.rpartition(".")[0]

			file_list.append(filename)

			print(f"filename_fullpath: {filename_fullpath}")
			print(f"filename: {filename}")
			print(f"filename_noext: {filename_noext}")
			print()

			invoke_drp(f"--out-ch-config {config_drp_outputchannelcfg} --force-atmos-file-dump --audio-out-file \"{filename_noext}.wav\" \"{filename}\"")

if user_input_mode == 2:
	for filename in file_list:
		filename_noext = filename.rpartition(".")[0]

		# Create folder in current directory named after input file
		create_dir(f"{directory}\\{filename_noext}")

		while True:
			time.sleep(1)
			try:
				if drp_process.poll() is not None:
					print("DRP is not running, beginning conversion of channels to multiple files...")
					break
			except:
				print("An exception has occurred, continuing anyways...")
				continue
		
		# Determine FFmpeg encoder and output file extension to use based on ini
		if config_ffmpeg_outputformat == "flac":
			ffmpeg_encoder = "flac"
			ffmpeg_ext = "flac"
		elif config_ffmpeg_outputformat == "wav":
			ffmpeg_encoder = "pcm_s16le"	# PCM signed 16-bit little-endian
			ffmpeg_ext = "wav"
		else:
			print("config_ffmpeg_outputformat is invalid, falling back to FLAC...")
			ffmpeg_encoder = "flac"
			ffmpeg_ext = "flac"
		
		# Split channels to different files
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c0|c1=c1[S]\" -map \"[S]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\01 Stereo.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=mono|c0=c2[C]\" -map \"[C]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\02 Center.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=mono|c0=c3[LFE]\" -map \"[LFE]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\03 Low Freq Effects.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c4|c1=c5[S]\" -map \"[S]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\04 Surround.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c6|c1=c7[RS]\" -map \"[RS]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\05 Rear Surround.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c8|c1=c9[W]\" -map \"[W]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\06 Wide.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c10|c1=c11[TF]\" -map \"[TF]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\07 Top Front.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c12|c1=c13[TM]\" -map \"[TM]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\08 Top Middle.{ffmpeg_ext}\" ")
		invoke_ffmpeg(f"-i \"{filename_noext}.wav\" -filter_complex \"[0:0]pan=stereo|c0=c14|c1=c15[TR]\" -map \"[TR]\" -c:a {ffmpeg_encoder} \"{filename_noext}\\09 Top Rear.{ffmpeg_ext}\" ")
	
	print("Complete! Exiting script in 3 seconds...")
	time.sleep(3)