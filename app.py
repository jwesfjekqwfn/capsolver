from flask import Flask, request, jsonify
from src import funcaptcha_challenger
import base64
from PIL import Image
import io

app = Flask(__name__)

def process_image(image_data, image_type):
    try:
        # Decode the base64 image data
        decoded_image_data = base64.b64decode(image_data)
        
        # Convert the decoded data into an image object
        image = Image.open(io.BytesIO(decoded_image_data))
        
        # Process the image using funcaptcha_challenger with the provided image type
        results = funcaptcha_challenger.predict(image, image_type)
        
        return results
    except Exception as e:
        # Log the error for debugging (optional)
        print(f"Error processing image: {e}")
        
        # Return None to indicate that an error occurred
        return None

@app.route('/createTask', methods=['POST'])
def process_image_route():
    data = request.json
    
    if 'image' not in data or 'type' not in data:
        return jsonify({"error": "Image and type must be provided"}), 400
    
    image_data = data['image']
    image_type = data['type']
    
    prediction_results = process_image(image_data, image_type)
    
    if prediction_results is None:
        return jsonify({"error": "An error occurred while processing the image"}), 500
    
    return jsonify({"result": prediction_results})

@app.route('/ping', methods=['GET'])
def ping_route():
    return jsonify({"message": "Pong"})

if __name__ == '__main__':
    app.run()  # Running Flask without debug mode
