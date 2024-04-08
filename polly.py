""" Convert text to speech with Amazon Polly. """

import boto3
import pyaudio

polly_client = boto3.client(service_name="polly", region_name="us-east-1", use_ssl=True)

py_audio = pyaudio.PyAudio()


def text_to_speech(input_text):
    result = polly_client.synthesize_speech(Text=input_text, OutputFormat="pcm", VoiceId="Lucia")

    stream_data(result["AudioStream"])


def stream_data(stream):

    chunk = 1042
    if stream:
        polly_stream = py_audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True,
        )

        while True:
            data = stream.read(chunk)
            polly_stream.write(data)

            if not data:
                stream.close()
                polly_stream.stop_stream()
                polly_stream.close()
                
                break
