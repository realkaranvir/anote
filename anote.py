import ollama
import time
import sys
import argparse
import whisper


def create_transcription(audio_file):
  print("Creating transcription...")
  start_time = time.time()
  model = whisper.load_model("small")
  result = model.transcribe(audio_file)
  with open("transcription.txt", "w") as file:
     file.write(result["text"])
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

   

