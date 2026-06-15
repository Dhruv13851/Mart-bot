import torch
import numpy as np
from silero_vad import (
    load_silero_vad,
    get_speech_timestamps
)


class VADService:

    def __init__(self):
        self.model = load_silero_vad()
        self.min_rms = 0.015
        self.min_speech_duration = 0.5

    def has_speech(
        self,
        audio: np.ndarray,
        sample_rate: int = 16000
    ) -> bool:

        if audio is None or len(audio) == 0:
            return False

        audio = audio.astype(np.float32)

        rms = np.sqrt(np.mean(audio ** 2))

        if rms < self.min_rms:
            return False

        wav = torch.from_numpy(audio)

        timestamps = get_speech_timestamps(
            wav,
            self.model,
            sampling_rate=sample_rate
        )

        if not timestamps:
            return False

        speech_samples = sum(
            ts["end"] - ts["start"]
            for ts in timestamps
        )

        speech_seconds = speech_samples / sample_rate

        return speech_seconds >= self.min_speech_duration