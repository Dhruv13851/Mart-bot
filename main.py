# from services.chatbot_service import (
#     ChatbotService
# )

# chatbot = ChatbotService()

# while True:

#     query = input(">>> ")

#     if query.lower() == "exit":
#         break

#     answer = chatbot.process_query(
#         query
#     )

#     print(answer)
from agents.math_agent import MathAgent

from chains.voice_chain import VoiceChain

from services.vad_service import VADService
from services.stt_service import STTService

from utils.audio_recorder import record_audio


def main():

    math_agent = MathAgent()

    voice_chain = VoiceChain(
        vad_service=VADService(),
        stt_service=STTService(),
         math_agent=math_agent

    )

    while True:

        print("\n" + "=" * 50)
        print("1. Text Query")
        print("2. Voice Query")
        print("3. Exit")
        print("=" * 50)

        choice = input(
            "\nChoose option: "
        ).strip()

        try:

            if choice == "1":

                query = input(
                    "\nEnter query: "
                ).strip()

                if not query:
                    print("Empty query.")
                    continue

            elif choice == "2":

                audio = record_audio()

                query = voice_chain.invoke(
                    audio=audio,
                    audio_path="temp.wav"
                )

                print(
                    f"\nTranscribed: {query}"
                )

            elif choice == "3":

                print("\nGoodbye!")
                break

            else:

                print(
                    "\nInvalid choice."
                )

                continue

            answer = math_agent.solve(
                query
            )

            print(
                f"\nAnswer: {answer}"
            )

        except Exception as e:

            print(
                f"\nError: {e}"
            )


if __name__ == "__main__":
    main()