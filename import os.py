import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
load_dotenv()


# Указываем имя переменной среды, значение которой вы хотите получить
variable_name = "OPENAI_API_KEY"

new_value = "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"

# Устанавливаем значение переменной среды
os.environ[variable_name] = new_value

# Получаем значение переменной среды
value = os.getenv(variable_name)

if value:
    print(f"Значение переменной {variable_name}:", value)
else:
    print(f"Переменная {variable_name} не установлена.")


print("Loading files in the load directory...")
# Load and save the index to disk
reader = SimpleDirectoryReader(input_dir="SOURCES_big/")
docs = reader.load_data()
index = VectorStoreIndex.from_documents(docs)

# Save the index to disk
index.storage_context.persist()
print("Done.")