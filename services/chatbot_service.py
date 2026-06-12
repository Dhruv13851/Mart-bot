from agents.math_agent import (
    MathAgent
)


class ChatbotService:

    def __init__(self):

        self.agent = MathAgent()

    def process_query(
        self,
        query: str
    ) -> str:

        return self.agent.solve(
            query
        )