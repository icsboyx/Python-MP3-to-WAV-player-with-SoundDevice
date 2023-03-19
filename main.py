import sounddevice as sd
import soundfile as sf
import io
import pydub
from pprint import pprint

# Query the available audio output devices
devices = sd.query_devices()
# Print the available devices and their indices
for idx, device in enumerate(devices):
    print(f"{idx + 1}. {device['name']}")

selected_device = None

# Prompt the user to select an audio output device
while not selected_device:
    try:
        choice = int(input("Select an audio output device: "))
        if 1 <= choice <= len(devices):
            selected_device = devices[choice - 1]
        else:
            print("Invalid choice. Please try again.")
    except ValueError:
        print("Invalid choice. Please try again.")

pprint(f"Valid choice: {selected_device}")  

# Set the selected device as the default audio output device
sd.default.device = selected_device['index']

# Load the mp3 audio file using pydub and convert it to wav format, resampling it to the selected device's default samplerate
mp3_data = pydub.AudioSegment.from_mp3('test.mp3')
mp3_data = mp3_data.set_frame_rate(int(selected_device['default_samplerate']))  
buffer = io.BytesIO()
mp3_data.export(buffer, format='wav')
buffer.seek(0)

# Load the wav audio data from the buffer using soundfile
data, samplerate = sf.read(buffer)

# Convert the audio data to float32 format (required by sounddevice)
data = data.astype('float32')

try:
    # Play the audio using the selected device and wait for it to finish playing
    sd.play(data, samplerate)
    sd.wait()
except KeyboardInterrupt:
    print('Interrupted by user')
finally:
    # Stop playback and close the audio device
    sd.stop()