# Anote

A simple python script which uses whisper and llama to help create notes.

## Installing Dependencies

To install dependencies you may want to create a virtual environment. This can be by running these commands in the root of the repo:  
`python3 -m venv venv`  
`source venv/bin/activate`
Make sure to activate the virtual environment before running the program

Then install the dependencies by running this command also in the root directory:  
`pip3 install -r requirements.txt`

## Running the Script

The script has three modes:

- `t` : Transcription only from an audio file
- `n` : Notes creation only from a text file
- `tn` : Both transcription and notes creation from an audio file

And one option:

- `--youtube` : Specifies if using a YouTube link instead of an mp3 file

Here's how to use each mode:

To create only a transcription from an audio file or youtube video:  
`python3 anote.py t audio_file.mp3`  
or  
`python3 anote.py t "your_youtube_link" --youtube`  
The transcription will be saved in the root directory as transcription.txt

To create only notes from a text file:  
`python3 anote.py n text_file.txt`  
The notes will be saved in the root directory as notes.txt

To create both:  
`python3 anote.py tn audio_file.mp3`  
or  
`python3 anote.py tn "your_youtube_link" --youtube`  
The transcription will be saved as transcription.txt and the notes as notes.txt. Both will be located in the root directory.

For the YouTube links, make sure to surround the link with quotes.

## Changing the model

I've found llama3.1 to be good for creating notes from the transcriptions considering it's size, but you may want to change the model. You can do this by changing the model name in the global variable at the top of the script. Check out the [List of models Ollama supports](https://ollama.com/library)
