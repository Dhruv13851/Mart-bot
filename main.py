from services.chatbot_service import (
    ChatbotService
)

chatbot = ChatbotService()

while True:

    query = input(">>> ")

    if query.lower() == "exit":
        break

    answer = chatbot.process_query(
        query
    )

    print(answer)