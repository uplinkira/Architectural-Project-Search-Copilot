from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pg_vector_store import create_pg_vector_store
from pg_loader import PGLoader


def add_novel_vector_to_pg(text_file_path: str):
    loader = TextLoader(text_file_path, encoding="utf-8")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(docs)
    print(f"读取了{len(all_splits)}条数据")
    vector_store = create_pg_vector_store("novel")
    vector_store.add_documents(all_splits)
    print("向量化完成")


def add_project_vector_to_pg():
    loader = PGLoader("project", "full_article")
    docs = loader.load()
    print(f"读取了{len(docs)}条数据")
    vector_store = create_pg_vector_store("project")
    vector_store.add_documents(docs)
    print("向量化完成")


if __name__ == "__main__":
    ...
    add_project_vector_to_pg()

    # path = os.path.join(os.getcwd(), "rag\测试用文档-小说.txt") # 注意，按照小说的体积要运行好几分钟
    # add_novel_vector_to_pg(path)
