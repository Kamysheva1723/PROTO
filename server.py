import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from flask import Flask, render_template, jsonify, request

variable_name = "OPENAI_API_KEY"

new_value = ""
os.environ[variable_name] = new_value

index = None
# set up the index, either load it from disk to create it on the fly
def initialise_index():
    global index
    print("Loading files in the load directory...")
    # Load and save the index to disk
    reader = SimpleDirectoryReader(input_dir="SOURCES_big/")
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs)

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

