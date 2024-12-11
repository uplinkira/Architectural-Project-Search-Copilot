from flask import Flask, request, jsonify, send_from_directory
import os
import re
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from pg_vector_store import create_pg_vector_store
from moonshot_chat import moonshot_chat
from sql_test import AskLainchainWithDb

app = Flask(__name__)

# 配置数据库和模型
DATABASE_POSTGRES_NAME = "spider"
DATABASE_POSTGRES_USER = "spider"
DATABASE_POSTGRES_PASSWORD = "8XR_M7.-*xzeQp4"
DATABASE_POSTGRES_HOST = "122.51.42.194"
DATABASE_POSTGRES_PORT = 54330
DATABASE_POSTGRES_URI = f"postgresql://{DATABASE_POSTGRES_USER}:{DATABASE_POSTGRES_PASSWORD}@{DATABASE_POSTGRES_HOST}:{DATABASE_POSTGRES_PORT}/{DATABASE_POSTGRES_NAME}"

db = SQLDatabase.from_uri(DATABASE_POSTGRES_URI)
os.environ["MOONSHOT_API_KEY"] = "sk-smlULyCmMfg3tdpms8bvT1u1tvu4YYymW9jg0mV2XQoV15pw"
llm = MoonshotChat()

# 问题到字段的映射
question_to_field_map = {
    "设计单位": "design_unit",
    "设计公司": "design_unit",
    "建筑类型": "project_types",
    "项目链接": "project_link",
    "项目图片链接": "project_image_link",
    "所在城市": "city",
    "所在国家": "country",
    "建筑层数": "building_floors",
    "建筑面积": "building_altitude",
    "材料": "building_materials",
    "总面积": "total_building_area_m2",
    "项目名称": "project_name",
    "整个文章": "full_article"
}

# RAG代码集成
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

# 对返回的结果进行Markdown链接和图片转换为HTML
def convert_markdown_links_to_html(text):
    """
    将 Markdown 格式的链接 `[链接文字](链接地址)` 和 `![图片描述](图片URL)` 转换为 HTML
    """
    # 正则表达式匹配 Markdown 链接
    link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    # 将 Markdown 链接转换为 HTML 格式的链接
    text = re.sub(link_pattern, r'<a href="\2" target="_blank">\1</a>', text)

    # 正则表达式匹配 Markdown 图片链接
    image_pattern = r'!\[([^\]]+)\]\((https?://[^\)]+)\)'
    # 将 Markdown 图片链接转换为 HTML 格式的图片标签
    text = re.sub(image_pattern, r'<img src="\2" alt="\1" />', text)

    return text

# 路由：加载HTML文件
@app.route('/')
def home():
    return send_from_directory(r'F:/project2/pythonProject2', 'question_web_1.html')

# 路由：处理一般查询（SQL 查询）
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "问题不能为空"}), 400

    answer = AskLainchainWithDb(user_question)
    return jsonify({"answer": answer})

# 路由：处理基于RAG的具体问题查询
@app.route("/ask_rag", methods=["POST"])
def ask_rag():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "问题不能为空"}), 400

    # 使用RAG进行检索并回答问题
    answer = rag("all_project", user_question)

    # 将Markdown格式的链接和图片转换为HTML
    answer = convert_markdown_links_to_html(answer)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
