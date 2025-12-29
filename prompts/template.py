from langchain_core.prompts import ChatPromptTemplate

augmented_prompt ="""
    Context:
        {context}
    
    Query:
        {query}
"""

prompt_template = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant who can help answer questions from given document context and the history of chat. Ground you answers to the given context and nothing else. Strictly Do not entertain any other type of questions"),
        ("human", augmented_prompt)
    ]
)

