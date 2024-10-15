import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = None

# Initialize the LLM object
def init_llm():
    global llm
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", 
        temperature=0.2,
        max_tokens=500
    )

# AI response generation function
def generate_ai_response(query, search_results):
    if llm is None:
        init_llm()
    
    # Join the relevant content from top search results (up to 3)
    context = "\n".join([f"- {result['full_content']}" for result in search_results[:3]])
    
    # Define the prompt template
    prompt_template = ChatPromptTemplate.from_template("""
    You are an AI assistant tasked with answering questions based on the provided context.
    Use the following pieces of context to answer the user's query. If you cannot find
    the answer in the context, say "I don't have enough information to answer that question."
    
    Context:
    {context}
    
    User Query: {query}
    
    AI Response:
    """)

    # Print the actual prompt text
    formatted_prompt = prompt_template.format_prompt(context=context, query=query)
    print("Actual Prompt Text:")
    print(formatted_prompt.to_string())

    # Create and run the LLM chain
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(query=query, context=context)
    return format_ai_response(response.strip())

def format_ai_response(ai_response):
    return {
        "path": None,  
        "name": "AI Response",  
        "content_snippet": ai_response[:100] + "...",  
        "content_length": len(ai_response),  
        "full_content": ai_response,  
        "highlighted_content": ai_response,  
        "occurrence_count": None  
    }
