import numpy as np
import sounddevice as sd
import soundfile as sf


SAMPLE_RATE = 16000
AUDIO_FILE = "temp.wav"


def record_audio():

    frames = []

    def callback(
        indata,
        frames,
        time,
        status
    ):
        audio_frames.append(
            indata.copy()
        )

    audio_frames = []

    input(
        "\nPress ENTER to start recording..."
    )

    print("Recording...")
    print("Press ENTER again to stop.")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        callback=callback
    )

    stream.start()

    input()

    stream.stop()
    stream.close()

    audio = np.concatenate(
        audio_frames,
        axis=0
    )

    sf.write(
        AUDIO_FILE,
        audio,
        SAMPLE_RATE
    )

    return audio.squeeze()