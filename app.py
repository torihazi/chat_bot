# ai_server/app.py
from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    
    def generate():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk and 'choices' in chunk:
                    content = chunk['choices'][0]['delta'].get('content', '')
                    if content:
                        yield content
        except Exception as e:
            yield str(e)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)