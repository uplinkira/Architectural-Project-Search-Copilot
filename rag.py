from pg_vector_store import create_pg_vector_store
from moonshot_chat import moonshot_chat
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


prompt_template = PromptTemplate.from_template(
    """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

You only need to answer three items to be sufficient
The link to the image corresponding to each answer item is written at the beginning

Question: {question} 
Context: {context} 
Answer:"""
)


def rag(collection_name: str, question: str) -> str:
    # 向量存储
    vector_store = create_pg_vector_store(collection_name)
    # 检索器
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | moonshot_chat
        | StrOutputParser()
    )
    return rag_chain.invoke(question)


if __name__ == "__main__":
    # result = rag("novel", "主角获得了哪些特殊奖励？")
    result = rag("all_project", "请帮我找找位于上海的学校项目")
    print(result)
