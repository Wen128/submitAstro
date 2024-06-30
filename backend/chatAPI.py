import google.generativeai as genai
from flask import Flask, jsonify, request

my_api_key = "AIzaSyCye2Bga-KDI0UjEZiIczyjQviE5wSSh5Q"

# setup flask
app = Flask(__name__)

@app.route('/')
def home():
    return "home"


genai.configure(api_key=my_api_key)
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
{
"category": "HARM_CATEGORY_HARASSMENT",
"threshold": "BLOCK_NONE"
},
{
"category": "HARM_CATEGORY_HATE_SPEECH",
"threshold": "BLOCK_NONE"
},
{
"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
"threshold": "BLOCK_NONE"
},
{
"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
"threshold": "BLOCK_NONE"
},
]

model = genai.GenerativeModel('gemini-1.5-flash')



def ask_AI(question, name, level):
    response = model.generate_content([
    "input: who are you?",
    "output: I am Mr. Bot.",
    "input: what can you do",
    "output: I can help you with answering question about malware and cybersecurity.",
    "input: You are a helpful robot that is expert in teaching everyone knowledge about malware, you will be always answer in a friendly tone.",
    "output: Ok I will",
    "input: What is Captain Pentagon",
    "output: Captain Pentagon is an android app developed by Peninsula Pro, It can used to scan malware, chating with me and do quiz!"
    "input: My name is ", name, ", My level of Cybersecurity Knowledege is ", level, ", always answer my questions with my name and reply suitable to my level",
    "output: Ok ", name, " what is the level means? "
    "input: Beginner means I am a beginner, tell me more friendly and very easy to understand and cannot more than 50 words, Advance means I am a junior in cybersecurity, I known quite more in cybersecurity, can tell me in more technical way and not more than 100 words, pro means I am pro in cybersecurity, tell me technical and details and not more than 150 words."
    "output: Ok, I am understand ", name,
    "input: ",question,
    ], safety_settings=safety_settings)

    return(response.text)




@app.route('/ask', methods=['POST'])
def handle_question():
    data = request.get_json()  # Get data from the POST request body
    if data and 'question' and 'name' in data:
        question = data['question']
        name = data['name']
        level = data['level']
        chatbot_response = ask_AI(question,name, level)
        return jsonify({'response': chatbot_response})
    else:
        return jsonify({'error': 'Missing question in request body'}), 400

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production