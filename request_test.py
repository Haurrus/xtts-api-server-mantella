import requests

# Define the URL of the API endpoint
set_tts_settings_url = 'http://127.0.0.1:8020/set_tts_settings/'  # Replace with the actual URL of your API

# Data to be sent in the request
data = {
    'temperature': 0.75,
    'length_penalty': 1.0,
    'repetition_penalty': 5.0,
    'top_k': 50,
    'top_p': 0.85,
    'speed': 1,
    'enable_text_splitting': True,
    'stream_chunk_size': 100
}

# Sending a POST request to the API endpoint
response = requests.post(set_tts_settings_url, json=data)

# Handling the response
if response.status_code == 200:
    print("Settings successfully applied")
else:
    print("Failed to apply settings")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

get_tts_settings_url = 'http://127.0.0.1:8020/get_tts_settings/'
get_tts_settings_response = requests.get(get_tts_settings_url)
print(get_tts_settings_response.json())

"""
# Switching the model
switch_model_url = 'http://127.0.0.1:8020/switch_model'
model_switch_response = requests.post(switch_model_url, json={"model_name": "femaledarkelf"})
print(model_switch_response.json())

# Sending a TTS request
tts_url = 'http://127.0.0.1:8020/tts_to_audio/'
tts_response = requests.post(tts_url, json={
    "text": "Hello How are you my friend ? I love chocolate and good behavior. Well… you see.",
    #"speaker_wav": "D:/Modelisation_IA/xtts-api-server/speakers/femaledarkelf",
    "speaker_wav": "femaledarkelf",
    "language": "en",
    "save_path": "D:/Modelisation_IA/xtts-api-server/output/voicelines.wav"
})
"""