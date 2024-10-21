from openai import OpenAI
from pydub import AudioSegment
import ollama
import time

client = OpenAI()
start_time = time.time()
recording = AudioSegment.from_mp3("short_lecture.mp3")
audio_segments = []
start_point = 0


print("Segmenting audio...")
i = 1
while (True):
    start_point = 24 * 60 * 1000 * (i - 1)
    end_point = 24 * 60 * 1000 * i
    

    if start_point > len(recording):
       break

    segment = recording[start_point:end_point]

    name = f"temp{i}.mp3"
    segment.export(name, format="mp3")
    audio_segments.append(name)
    i += 1

print("Transcribing audio...")
with open("transcription.txt", "w") as file:
  for name in audio_segments:
    audio_file = open(name, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file, 
      response_format="text"
    )
    audio_file.close()
    file.write(transcription)
    time.sleep(2)

with open("transcription.txt", "r") as file:
   transcription = file.read()


print("Creating notes...")
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f"Creates bullet point notes for the following transcription of my lecture. The notes can be as long as needed to gather the all the info:\n {transcription}",
  },
])


with open("notes.txt", "w") as file:
   file.write(response["message"]["content"])

end_time = time.time()

print(f"Notes created in {(end_time - start_time):.2f} seconds")
