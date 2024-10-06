from flask import Flask, request, jsonify
from flask_cors import CORS
from haystack import Pipeline
from haystack.document_stores import SQLDocumentStore
from haystack.nodes import OllamaReader
from config import Config

app = Flask(__name__)
CORS(app)

# Initialize DocumentStore
document_store = SQLDocumentStore(
  url=Config.DATABASE_URL,
  index="chat_logs",
  embedding_field=None,  # Adjust if using embeddings
  embedding_dim=None,
  excluded_meta_data=["embedding"]
)

# Initialize Ollama Reader
try:
  reader = OllamaReader(
      host=Config.MODEL_HOST,
      port=Config.MODEL_PORT,
      model_name="llama3.2"  # Replace with the actual model name
  )
except Exception as e:
  print(f"Error initializing OllamaReader: {e}")
  reader = None

# Create Pipeline
pipeline = Pipeline()
if reader:
  pipeline.add_node(component=reader, name="ollama_reader", inputs=["Query"])
else:
  raise Exception("OllamaReader not initialized.")

@app.route('/api/chat', methods=['POST'])
def chat():
  data = request.get_json()
  if not data or 'message' not in data:
      return jsonify({"error": "Invalid input"}), 400

  user_message = data['message']

  try:
      prediction = pipeline.run(query=user_message, params={"ollama_reader": {"top_k": 1}})
      reply = prediction['answers'][0].answer if prediction['answers'] else "I'm sorry, I don't have an answer to that."

      # Log to database
      chat_log = {
          "user_input": user_message,
          "assistant_response": reply
          # "timestamp" is automatically added by the database
      }
      document_store.write_documents([chat_log])

      return jsonify({"reply": reply}), 200
  except Exception as e:
      return jsonify({"error": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
  try:
      results = document_store.get_all_documents()
      logs = [
          {
              "id": doc.id,
              "user_input": doc.meta.get("user_input"),
              "assistant_response": doc.meta.get("assistant_response"),
              "timestamp": doc.meta.get("timestamp")
          }
          for doc in results
      ]
      return jsonify({"logs": logs}), 200
  except Exception as e:
      return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)