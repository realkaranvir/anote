import ollama
import time
import sys
import argparse
import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os


ollama_model = "llama3.1"
SAVE_PATH = "./"


def download_youtube_video_as_mp3(url):
  
  try:
     yt = YouTube(url, on_progress_callback = on_progress)
  except:
     print("Error downloading youtube video")

  print(f"Downloading '{yt.title}'...")
  ys = yt.streams.get_audio_only()
  file_name = ys.download(mp3=True)
  file_name = os.rename(file_name, "downloaded")
  return file_name


def create_transcription(audio_file):
  print("Creating transcription...")
  start_time = time.time()
  model = whisper.load_model("small")
  result = model.transcribe(audio_file)
  with open(f"{SAVE_PATH}transcription.txt", "w") as file:
     file.write(result["text"])
  end_time = time.time()
  print(f"File transcribed in {(end_time - start_time):.2f} seconds")


def create_notes(text):
  start_time = time.time()

  # Remove notes.txt if it already exists
  if os.path.exists(f"{SAVE_PATH}notes.txt"):
    os.remove(f"{SAVE_PATH}notes.txt")

  print("Creating notes...")
  
  with open(text, "r") as file:
    transcription = file.read()

  words = transcription.split()

  # Split the transcription into groups of 1000 words
  transcript_sections = [words[i:i + 1000] for i in range(0, len(words), 1000)]
  
  for section in transcript_sections:
    max_retries = 3  # Set the maximum number of retries
    attempt = 0
    response = None

    section_text = " ".join(section)
    while attempt < max_retries:
        try:
            response = ollama.chat(model=ollama_model, messages=[
                {
                    'role': 'user',
                    'content': f"Create bullet point notes for the following transcription of a video. Please make the notes as detailed as possible. Here is the transcription:\n {section_text}",
                },
            ])
            break  # Exit loop if attempt succeeds
        

        except ollama.ResponseError as e:
            print('Error:', e.error)
            if e.status_code == 404:
                print(f"Model '{ollama_model}' not found. Pulling the model...")
                ollama.pull(ollama_model)
                attempt += 1  # Increment the attempt counter
                print(f"Retrying... ({attempt}/{max_retries})")
            else:
                print("An unexpected error occurred. Aborting.")
                return

    if response is None:
        print("Failed to create notes after multiple attempts.")
        return 



    with open(f"{SAVE_PATH}notes.txt", "a") as file:
      file.write(response["message"]["content"])

  end_time = time.time()

  print(f"Notes created in {(end_time - start_time):.2f} seconds")


def main():
    start_time = time.time()
  # Create the parser
    parser = argparse.ArgumentParser(description="Process an MP3 file or youtube link with options for transcription or note creation.")
    
    # Add the positional argument for the option (either 't', 'n', or 'tn')
    parser.add_argument("option", choices=['t', 'n', 'tn'], help="Choose 't' for transcription, 'n' for notes, or 'tn' for both.")
    
    # Add the positional argument for the file
    parser.add_argument("file", type=str, help="The MP3 file or YouTube link to process.")

    # Add the optional flag to indicate if the input is a YouTube link
    parser.add_argument("--youtube", action="store_true", help="Specify if the input is a YouTube link.")

    # Parse the arguments
    args = parser.parse_args()

    if args.youtube:
      print(args.file)
      audio_file = download_youtube_video_as_mp3(args.file)
    else:
      audio_file = args.file

    # Execute based on the option
    if args.option == 't':
        create_transcription(audio_file)
    elif args.option == 'n':
        create_notes(args.file)
    elif args.option == 'tn':
        create_transcription(audio_file)
        create_notes("transcription.txt")
    else:
        print("Invalid option.")
        sys.exit(1)
    end_time = time.time()
    print(f"Total time taken: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
   main()

   

