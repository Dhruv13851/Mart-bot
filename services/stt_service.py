from faster_whisper import WhisperModel


class STTService:

    def __init__(self):

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(
        self,
        audio_path: str
    ) -> str:

        segments, _ = self.model.transcribe(
            audio_path,
            beam_size=5,
            language="en"
        )

        return " ".join(
            segment.text
            for segment in segments
        ).strip()