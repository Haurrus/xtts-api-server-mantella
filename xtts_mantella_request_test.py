import argparse
import requests
import io
import os
import sys

# Setup argument parser
parser = argparse.ArgumentParser(description='Script to send TTS requests.')
parser.add_argument('--ip', '-i', default='127.0.0.1', help='IP address of the server. Default is 127.0.0.1.')
parser.add_argument('--port', '-p', default=8020, type=int, help='Port of the server. Default is 8020.')
parser.add_argument('--text', '-t', required=False, help='Text to convert to speech. Required.')
parser.add_argument('--speaker_wav', '-sw', required=False, help='Speaker WAV file. Required.')
parser.add_argument('--language', '-l', default='en', help='Language of the text. Default is en.')
parser.add_argument('--file_path', '-fp', default='.', help='Path where the output file will be saved. Default is current directory.')
parser.add_argument('--switch_model', '-sm', required=False, help='Model to switch to. If blank, no model switch is attempted.')

args = parser.parse_args()

# Check if the essential arguments 'text' and 'speaker_wav' are missing
if args.text is None or args.speaker_wav is None:
    parser.print_help()
    sys.exit(1)

# Only switch models if switch_model argument is provided
if args.switch_model:
    switch_model_url = f'http://{args.ip}:{args.port}/switch_model'
    model_switch_response = requests.post(switch_model_url, json={"model_name": args.switch_model})
    print(model_switch_response.json())

# Preparing TTS request URL
tts_url = f'http://{args.ip}:{args.port}/tts_to_audio/'

# Sending a TTS request
tts_response = requests.post(tts_url, json={
    "text": args.text,
    "speaker_wav": args.speaker_wav,
    "language": args.language
})

# Assuming tts_response.content is your binary data.
tts_content = io.BytesIO(tts_response.content)

# Generate the full path for the output file
full_file_path = os.path.join(args.file_path, "output.wav")

# Open a file in binary write mode and write the content of the BytesIO object.
with open(full_file_path, 'wb') as file_output:
    tts_content.seek(0)  # Go to the beginning of the BytesIO object.
    file_output.write(tts_content.read())

print(f"File saved to {full_file_path}")
