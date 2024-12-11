from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from m3e_embeddings import M3eEmbeddings
from db_constants import DATABASE_POSTGRES_URI_PSYCOPG

embeddings = M3eEmbeddings()


def create_pg_vector_store(collection_name: str) -> PGVector:
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=DATABASE_POSTGRES_URI_PSYCOPG,  # 写死了
        use_jsonb=True,
    )
    return vector_store
