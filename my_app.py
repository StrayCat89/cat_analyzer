from flask import Flask, request, jsonify, send_from_directory
import requests
import os

print("Starting the Flask app...")

app = Flask(__name__)

@app.route('/')
def serve_index():
    try:
        print("Serving index2.html")
        return send_from_directory('.', 'index2.html')
    except Exception as e:
        print(f"Error serving index2.html: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_url = data['image_url']
        prompt = data['prompt']
        print(f"Received image_url: {image_url} and prompt: {prompt}")

        response = requests.post("https://michaelbutler.app.modelbit.com/v1/prompt_llava/latest",
                                 json={"data": [image_url, prompt]})
        response.raise_for_status()
        api_response = response.json()
        print(f"Response from API: {api_response}")

        # Extract the 'data' field from the API response
        answer = api_response.get('data', 'No answer found')
        
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Running the app...")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
