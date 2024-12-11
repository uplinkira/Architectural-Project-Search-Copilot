# Architecture Project Search System

A web-based system that allows users to search and query architectural project information using both SQL and RAG (Retrieval-Augmented Generation) approaches.

## Features

- **SQL-based Search**: Query projects based on specific criteria like location, building area, materials etc.
- **RAG-based Detailed Queries**: Ask natural language questions about project details and get AI-generated responses
- **Vector Store Integration**: Uses PGVector for efficient similarity search
- **Web Interface**: Clean and intuitive UI with split-panel design
- **Moonshot AI Integration**: Leverages Moonshot's LLM capabilities for natural language understanding

## Technical Stack

- **Backend**:
  - Flask (Web Framework)
  - Langchain (LLM Integration)
  - PostgreSQL (Database)
  - PGVector (Vector Store)
  - M3E Embeddings (Text Embeddings)

- **Frontend**:
  - HTML/CSS/JavaScript
  - Responsive Design

## Key Components

- `app_1.py`: Main Flask application with API endpoints
- `add_document_to_pg.py`: Utilities for adding documents to vector store
- `pg_vector_store.py`: PostgreSQL vector store integration
- `rag.py`: RAG implementation for detailed queries
- `sql_test.py`: SQL query generation and execution
- `question_web_1.html`: Web interface

## Setup

1. Configure PostgreSQL database with the following credentials: 

```python
DATABASE_POSTGRES_NAME = "spider"
DATABASE_POSTGRES_USER = "spider"
DATABASE_POSTGRES_PASSWORD = "your_password"
DATABASE_POSTGRES_HOST = "your_host"
DATABASE_POSTGRES_PORT = your_port
```
2. Install required Python packages:

```bash
pip install flask langchain psycopg2-binary sentence-transformers
```

3. Set up Moonshot API key:
```python
os.environ["MOONSHOT_API_KEY"] = "your_api_key"
```


## Usage

1. Start the Flask server:
```bash
python app_1.py
```

2. Access the web interface at `http://localhost:5000`

3. Use the left panel for SQL-based project searches:
   - Enter queries like "Find projects in Shanghai with area between 300-600 square meters"
   - Results will be displayed in cards showing project details

4. Use the right panel for detailed RAG-based queries:
   - Ask specific questions about projects like "What's the design concept of Anhui Art Museum?"
   - The AI assistant will provide detailed responses based on the project documentation

## Project Structure
Root
├── add_document_to_pg.py # Document processing utilities
├── app_1.py # Main Flask application
├── m3e_embeddings.py # Text embedding implementation
├── moonshot_chat.py # Moonshot AI integration
├── pg_loader.py # PostgreSQL data loader
├── pg_vector_store.py # Vector store implementation
├── question_web_1.html # Web interface
├── rag.py # RAG implementation
└── sql_test.py # SQL query handling

## Features in Detail

### SQL Search
- Supports complex queries combining multiple criteria
- Real-time query processing
- Results displayed in an easy-to-read card format
- Includes project images and links

### RAG Search
- Natural language query processing
- Context-aware responses
- Integration with project documentation
- Intelligent answer generation

## Notes

- The system supports both Chinese and English queries
- Vector store uses M3E embeddings optimized for Chinese language
- The web interface displays project information including links and images
- Results are limited to prevent overwhelming responses
- Responsive design works on both desktop and mobile devices

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Thanks to Moonshot AI for providing the LLM capabilities

- Thanks to the Langchain community for the excellent tools and documentation

- Thanks to the Smart Design R&D Institute of China Eastern Architectural Design & Research Institute for sharing their workflow

- Thanks to the team members who participated in the 2024 CDAC Computational Design Symposium and the Annual Conference of Computational Design Academic Committee of Chinese Architectural Society: Yuqi Shangguan, Yuanyuan Wu, Youpeng Lin, Xinya Deng

