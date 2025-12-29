import os
from services.agent import Agent
from services.vectorstore import Vectorstore
from langchain.messages import HumanMessage
from prompts.template import prompt_template

from dotenv import load_dotenv

load_dotenv()

# Initiaize agent and vectorstore
agent = Agent(system_prompt="You are a helpful assistant who can help answer questions from given document context and the history of chat. Ground you answers to the given context and nothing else. Strictly Do not entertain any other type of questions")
agent.initialize_agent()

vectorstore = Vectorstore(db_path= "./chromadb_data")
vectorstore.initialize_vectorstore()


def ask_llm(prompt):
    config={
        "configurable": {"thread_id": "1"}
    }
    documents = vectorstore.similarity_search(prompt)
    content = [doc.page_content for doc in documents]
    context = "\n> ".join(content)
    augmented_prompt = prompt_template.invoke(input={"context": context, "query": prompt})
    response = agent.invoke(augmented_prompt, config)
    print(response["messages"][-1].content)


def uplaod_documents():
    path = input("Enter path: ")
    vectorstore.add_documents(path=path)


def clear_database():
    vectorstore.reset_collection()


def main():

    while True:
        print("What do you want to do?\n")
        print("1. Upload Documents")
        print("2. Chat with LLM")
        print("3. Reset DB")
        user_choice = int(input("Enter choice: "))
        match user_choice:
            case 1:
                uplaod_documents()
            case 2:
                while True:
                    user_input = input("Ask: ")
                    if user_input.lower() == "exit":
                        break
                    ask_llm(user_input)
            case 3:
                clear_database()
            case _:
                print("Invalid choice")


if __name__=="__main__":
    main()

