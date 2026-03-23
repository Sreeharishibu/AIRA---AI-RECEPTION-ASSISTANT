# stt_utils.py
import os
import wave
import subprocess
from django.conf import settings

from vosk import Model, KaldiRecognizer

_vosk_model = None


def get_vosk_model():
    """
    Load the Vosk model once (lazy singleton).
    """
    global _vosk_model
    if _vosk_model is None:
        model_path = getattr(settings, "VOSK_MODEL_PATH", None)
        if not model_path or not os.path.isdir(model_path):
            raise RuntimeError(f"Invalid VOSK_MODEL_PATH: {model_path}")
        _vosk_model = Model(model_path)
    return _vosk_model


def convert_to_wav_16k_mono(src_path, dst_path):
    """
    Use ffmpeg to convert arbitrary audio file to 16kHz mono WAV (PCM16).
    """
    cmd = [
        "ffmpeg",
        "-y",              # overwrite output
        "-i", src_path,    # input file
        "-ar", "16000",    # sample rate
        "-ac", "1",        # mono
        "-f", "wav",
        dst_path,
    ]
    # Run ffmpeg quietly
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def transcribe_audio(audio_path: str) -> str:
    """
    Given an audio file path, convert to 16k mono wav, and run Vosk STT.
    Returns recognized text (or empty string).
    """
    model = get_vosk_model()

    # 1) Convert input file to a temporary WAV
    wav_path = os.path.splitext(audio_path)[0] + "_16k.wav"
    convert_to_wav_16k_mono(audio_path, wav_path)

    # 2) Run Vosk on the WAV
    wf = wave.open(wav_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
        wf.close()
        raise RuntimeError("Converted WAV is not 16-bit mono")

    rec = KaldiRecognizer(model, wf.getframerate())

    result_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = rec.Result()
            # part is JSON like {"text": "hello world"}
            # We just accumulate final results
        # else: partial = rec.PartialResult()
    final = rec.FinalResult()
    wf.close()

    # final is JSON → extract "text"
    import json
    try:
        final_json = json.loads(final)
        result_text = final_json.get("text", "").strip()
    except Exception:
        result_text = ""

    # Optional: clean up temp wav
    try:
        os.remove(wav_path)
    except OSError:
        pass

    return result_text
