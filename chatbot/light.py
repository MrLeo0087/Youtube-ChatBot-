from langgraph.graph import StateGraph,START,END
from model_choice.promt import default_rag_prompt
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

chat_model = 'gemini-2.5-flash-lite'

memory = InMemorySaver()

def chat(api,query,context,thread_id = 'user_123'):
    class LightLLM(TypedDict):
        messages: Annotated[list[BaseMessage],add_messages]

    llm = ChatGoogleGenerativeAI(
            google_api_key=api,
            model=chat_model, 
            temperature=0.2,           
            max_output_tokens=1000,                
        )  

    chain = default_rag_prompt | llm
        
    def chatbot(state: LightLLM):
        last_message = state['messages'][-1].content
        memory_llm = state['messages'][-20:]
        response = chain.invoke({
            'context':context,
            'question':last_message,
            'history':memory_llm[:-1]
        })
        return {'messages':[response]}
    
    graph = StateGraph(LightLLM)
    graph.add_node('chatbot',chatbot)
    graph.add_edge(START,'chatbot')
    graph.add_edge('chatbot',END)

    config = {"configurable":{"thread_id":thread_id}}

    workflow = graph.compile(checkpointer=memory)
    question = {'messages':[HumanMessage(content=query)]}
    response = workflow.invoke(question,config=config)
    return response['messages'][-1].content
