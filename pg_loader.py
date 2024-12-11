from collections.abc import Iterator
import psycopg2
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from db_constants import DATABASE_POSTGRES_URI


class PGLoader(BaseLoader):
    def __init__(self, table_name: str, column_name: str):
        self.table_name = table_name
        self.column_name = column_name

    def lazy_load(self) -> Iterator[Document]:
        conn = psycopg2.connect(DATABASE_POSTGRES_URI)  # 写死了
        cur = conn.cursor()
        cur.execute(f"SELECT id,{self.column_name} FROM {self.table_name}")
        rows = cur.fetchall()
        for row in rows:
            id = int(row[0])
            content = str(row[1])
            doc = Document(page_content=content, metadata={"id": id})
            yield doc
        cur.close()
        conn.close()
