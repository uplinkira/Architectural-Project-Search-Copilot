import os
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

DATABASE_POSTGRES_NAME = "spider"
DATABASE_POSTGRES_USER = "spider"
DATABASE_POSTGRES_PASSWORD = "8XR_M7.-*xzeQp4"
DATABASE_POSTGRES_HOST = "122.51.42.194"
DATABASE_POSTGRES_PORT = 54330

DATABASE_POSTGRES_URI = f"postgresql://{DATABASE_POSTGRES_USER}:{DATABASE_POSTGRES_PASSWORD}@{DATABASE_POSTGRES_HOST}:{DATABASE_POSTGRES_PORT}/{DATABASE_POSTGRES_NAME}"

db = SQLDatabase.from_uri(DATABASE_POSTGRES_URI)
os.environ["MOONSHOT_API_KEY"] = "sk-smlULyCmMfg3tdpms8bvT1u1tvu4YYymW9jg0mV2XQoV15pw"
llm = MoonshotChat()

# 提问到数据库字段的映射
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

# 用于生成SQL查询的模板
write_query_template = PromptTemplate.from_template(
    """你是一个SQL专家，你需要写一个 {dialect} 查询语句。
你只需要查询{top_k}条数据。
注意，你的回答必须只包含SQL语句，不要包含任何其他信息。
注意，你的回答必须是一个合法的SQL查询语句。
注意，不要用Markdown或者其他格式包裹你的SQL语句。

你使用的数据库的表格信息如下：
{table_info}

你需要根据以下问题生成SQL查询：
{input}
"""
)

# 创建 SQL 查询链
write_query = create_sql_query_chain(llm, db, write_query_template)  # 返回一个SQL语句
execute_query = QuerySQLDataBaseTool(db=db)

# 答案提示模板，修改格式输出规则
answer_prompt = PromptTemplate.from_template(
    """根据以下用户问题、SQL查询和SQL结果，回答用户的问题。
如果SQL结果不足以回答问题，或者无法正确解析问题，请直接说“不知道”。
你只能根据SQL查询结果提供的信息来回答问题，不能提供任何额外的内容。
你需要使用中文回答。

你需要根据以下格式输出每一个项目的答案：

    1.-项目名称：
      -项目所在地：
      -建筑总面积：
      -建筑材料：
      -项目链接：
      -项目图片：

问题：{question}
SQL 查询：{query}
SQL 结果：{result}

回答：
"""
)


# 移除 SQL 查询中的 markdown 格式
def remove_markdown_in_sql(query: str) -> str:
    return query.replace("```sql", "").replace("```", "").strip()


clean_query = RunnablePassthrough(remove_markdown_in_sql)

# 查询链：生成查询 -> 清洗查询 -> 执行查询 -> 答案
chain = (
        RunnablePassthrough.assign(query=write_query | clean_query)
        .assign(result=itemgetter("query") | execute_query)
        | answer_prompt
        | llm
        | StrOutputParser()
)


# 自定义函数：提取提问中的关键词，并映射到相应的数据库字段
def map_question_to_field(question: str):
    for key, field in question_to_field_map.items():
        if re.search(key, question, re.IGNORECASE):  # 匹配问题中包含的关键词
            return field
    return None


# 主函数，用于接收用户问题并返回答案
def AskLainchainWithDb(text: str) -> str:
    # 获取问题的字段映射
    field = map_question_to_field(text)
    if not field:
        return "不知道"  # 如果无法映射字段，则回答“不知道”

    # 将映射的字段加入查询逻辑
    query = f"""
    SELECT 
        project_name, 
        design_unit, 
        project_types, 
        project_link, 
        project_image_link, 
        city, 
        country, 
        building_floors, 
        total_building_area_m2
    FROM projects 
    WHERE {field} = '{text}' 
    LIMIT 3;  -- 只查询前3条，避免返回过多数据
    """

    # 执行查询并返回结果
    result = chain.invoke({"question": text, "query": query})
    return result


if __name__ == "__main__":
    result = AskLainchainWithDb("帮我查一下主要材料是玻璃，且位于上海的项目有哪些?")
    print(result)
