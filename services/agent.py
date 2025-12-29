import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

class Agent:
    def __init__(self, system_prompt):
        self.model_name=os.getenv("OPENAI_CHAT_MODEL")
        self.system_prompt=system_prompt

    def _instantiate_chat_model(self):
        model = init_chat_model(
            model=self.model_name,
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            timeout=10
        )

        return model

    def initialize_agent(self):
        chat_model = self._instantiate_chat_model()
        self.agent=create_agent(
            model=chat_model,
            tools=[],
            system_prompt=SystemMessage(self.system_prompt),
            checkpointer=InMemorySaver()
        )
    
    def invoke(self, prompt, config):
        return self.agent.invoke(prompt, config)
    

