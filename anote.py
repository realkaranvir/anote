from openai import OpenAI
from pydub import AudioSegment
import ollama
import time
import sys
import argparse


def create_transcription(audio_file):
  client = OpenAI()
  start_time = time.time()
  recording = AudioSegment.from_mp3(audio_file)
  #Add conversion to wav files here
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

  #Add cleanup of temp files
  end_time = time.time()
  print(f"File transcribed in {(end_time - start_time):.2f} seconds")


def create_notes(text):
  start_time = time.time()
  with open(text, "r") as file:
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


def main():
  # Create the parser
    parser = argparse.ArgumentParser(description="Process an MP3 file with options for transcription or note creation.")
    
    # Add the positional argument for the option (either 't', 'c', or 'tc')
    parser.add_argument("option", choices=['t', 'n', 'tn'], help="Choose 't' for transcription, 'n' for notes, or 'tn' for both.")
    
    # Add the positional argument for the file
    parser.add_argument("file", type=str, help="The MP3 file to process.")

    # Parse the arguments
    args = parser.parse_args()

    # Execute based on the option
    if args.option == 't':
        create_transcription(args.file)
    elif args.option == 'n':
        create_notes(args.file)
    elif args.option == 'tn':
        create_transcription(args.file)
        create_notes("transcription.txt")
    else:
        print("Invalid option.")
        sys.exit(1)

if __name__ == "__main__":
   main()

   

