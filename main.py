from services import AgentBuilder
from langchain.messages import HumanMessage, AIMessage



agent_builder = AgentBuilder(model_name="gpt-4.1-mini", system_prompt="You are a helpful assistant.")
agent = agent_builder.create_agent()


agent_state={
    "messages":[
        HumanMessage("Hello"),
        AIMessage("Hello, what can i do for you?")
    ]
}
config={
    "configurable": {"thread_id": "1"}
}

while True:
    user_input = input("Enter: ")
    agent_state["messages"].append(HumanMessage(user_input))
    response = agent.invoke(agent_state, config)
    print(response["messages"][-1].content)



