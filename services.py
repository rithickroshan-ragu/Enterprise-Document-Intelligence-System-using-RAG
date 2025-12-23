import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()

class AgentBuilder:
    def __init__(self, model_name, system_prompt):
        self.model_name=model_name
        self.system_prompt=system_prompt

    def _instantiate_chat_model(self):
        model = init_chat_model(
            model=self.model_name,
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            timeout=10
        )

        return model

    def create_agent(self):
        chat_model = self._instantiate_chat_model()
        agent=create_agent(
            model=chat_model,
            tools=[],
            system_prompt=SystemMessage(self.system_prompt),
            checkpointer=InMemorySaver()
        )

        return agent
    
    

