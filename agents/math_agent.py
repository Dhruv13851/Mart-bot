from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from config.llm import get_llm

from prompts.math_agent_prompt import (
    SYSTEM_PROMPT
)

from tools.calculator_tool import (
    math_solver
)


class MathAgent:

    def __init__(self):

        self.llm = get_llm()

        self.tools = [
            math_solver
        ]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT
                ),
                (
                    "human",
                    "{input}"
                ),
                (
                    "placeholder",
                    "{agent_scratchpad}"
                )
            ]
        )

        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=False
        )

    def solve(
        self,
        query: str
    ) -> str:

        response = self.executor.invoke(
            {
                "input": query
            }
        )

        return response["output"]