import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from flask import Flask, render_template, jsonify, request
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.node_parser import SimpleNodeParser





variable_name = "OPENAI_API_KEY"

new_value = ""
os.environ[variable_name] = new_value

index = None
# set up the index, either load it from disk to create it on the fly
def initialise_index():
    global index
    # check if storage already exists
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("sources").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)

        # Cоздаем парсер
        parser = SimpleNodeParser()

        # Разбиваем на ноды
        nodes = parser.get_nodes_from_documents(documents)

        # Создаем индекс
        index = VectorStoreIndex([])

        # Индексируем ноды
        index.insert_nodes(nodes)


    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)



# get path for GUI
gui_dir = os.path.join(os.path.dirname(__file__), 'gui')
if not os.path.exists(gui_dir):
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui')

# start server
server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)

# initialise index
initialise_index()

@server.route('/')
def landing():
    return render_template('index.html')

@server.route('/query', methods=['POST'])
def query():
    global index
    data = request.json


    query_engine = index.as_query_engine()
    response = query_engine.query(data["input"])

    return jsonify({'query': data["input"],
                    'response': str(response),
                    'source': response.get_formatted_sources()})

