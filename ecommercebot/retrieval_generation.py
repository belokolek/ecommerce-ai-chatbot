from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from ecommercebot.data_ingest import ingestData
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')


def generation(vectorStore):
    retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatGroq(api_key=GROQ_API_KEY)

    chain = (
        {"context" : retriever, "question" : RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )

    return chain


if __name__ == "__main__":
    vectorStore = ingestData("done")
    chain = generation(vectorStore)
    print(chain.invoke("can you tell me the best bluetooth buds?"))