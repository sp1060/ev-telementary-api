from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Global threshold tracker variable matching your edge state
current_threshold = 0.0416

@app.route('/api/v1/sync', methods=['POST'])
def sync_telemetry():
    global current_threshold
    try:
        # Parse incoming JSON array from virtual ESP32
        data = request.get_json(force=True)
        print("\n📥 [CLOUD INGESTION] New Telemetry Packet Received:")
        print(data)
        
        # Structure the automated response payload back to Wokwi
        response_payload = {
            "status": "SUCCESS",
            "message": "Telemetry vectors successfully committed to database.",
            "updated_threshold": current_threshold
        }
        return jsonify(response_payload), 200

    except Exception as e:
        print(f"❌ Processing Error: {str(e)}")
        return jsonify({"status": "ERROR", "message": "Malformed payload structure"}), 400

@app.route('/', methods=['GET'])
def health_check():
    return "🚀 Telemetry Pipeline Cloud Server is running live on Render!", 200

if __name__ == '__main__':
    # Render binds your app dynamically to a designated internal port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
