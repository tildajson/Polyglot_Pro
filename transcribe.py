""" Transcribe speech to text with Amazon Transcribe. """

from translate import translate_text
from polly import text_to_speech

import asyncio
import sounddevice

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent, TranscriptResultStream


class TranscriptEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream: TranscriptResultStream,
                 language_input, language_output):
        super().__init__(transcript_result_stream)
        self.language_input = language_input
        self.language_output = language_output

        async def handle_transcript_event(self, transcript_event: TranscriptEvent):
            results = transcript_event.transcript.results

            if len(results) > 0:
                transcript = results[0].alternatives[0].transcript

                if hasattr(results[0], "is_partial") and results[0].is_partial == False:
                    print("Transcript", transcript)

                    translated_text = translate_text(transcript, self.language_input,
                                                     self.language_output)
                    print("Translated text:", translated_text)

                    text_to_speech(translated_text)


async def mic_stream():
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()


    def callback(in_data, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(in_data), status))

    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024*2,
        dtype="int16",
    )

    with stream:
        while True:
            in_data, status = await input_queue.get()
            yield in_data, status


async def write_chunks(stream):
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe(language_input, language_output):
    client = TranscribeStreamingClient(region="us-east-1")

    stream = await client.start_stream_transcription(
        language_code=language_input,
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    handler = TranscriptEventHandler(stream.output_stream, language_input, language_output)
    await asyncio.gather(write_chunks(stream), handler.handle_events())


def transcribe_audio(language_input, language_output):
    loop = asyncio.get_event_loop()
    task = loop.create_task(basic_transcribe(language_input, language_output))
    loop.run_until_complete(task)
    loop.close()

    return task.result()
    