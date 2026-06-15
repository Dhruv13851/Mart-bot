from langchain_core.runnables import RunnableLambda


class VoiceChain:

    def __init__(
        self,
        vad_service,
        stt_service,
        math_agent
    ):

        self.chain = (
            RunnableLambda(
                self._validate_audio
            )
            |
            RunnableLambda(
                self._speech_to_text
            )
            |
            math_agent.runnable
        )

        self.vad = vad_service
        self.stt = stt_service

    def _validate_audio(
        self,
        payload: dict
    ):

        if not self.vad.has_speech(
            payload["audio"]
        ):
            raise ValueError(
                "No speech detected."
            )

        return payload

    def _speech_to_text(
        self,
        payload: dict
    ):

        text = self.stt.transcribe(
            payload["audio_path"]
        )

        return {
            "input": text
        }

    def invoke(
        self,
        audio,
        audio_path
    ):

        return self.chain.invoke(
            {
                "audio": audio,
                "audio_path": audio_path
            }
        )