
import os
from flask import Flask, request, jsonify, send_file
from PIL import Image
import pytesseract
import tempfile
import uuid
import openai
from gtts import gTTS

# Configure
OPENAI_API_KEY = "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";
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
TTS_FOLDER = "./tts"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TTS_FOLDER, exist_ok=True)

@app.route("/upload-image", methods=["POST"])
def upload_image():
    # We expect raw JPEG body from the ESP32 POST
    data = request.get_data()
    if not data:
        return jsonify({"error": "No data"}), 400
    fname = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
    with open(fname, "wb") as f:
        f.write(data)
    # Run OCR
    try:
        img = Image.open(fname)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        text = ""
    # Call OpenAI for summary (example)
    prompt = f"Extract the text from the image and provide a short summary (max 40 words), then a simple translation to Yoruba. Text:\n\n{text}"
    ai_resp = ""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", # adjust to available model; or gpt-4o if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant for scanned text. Return a JSON with keys 'summary' and 'translation'."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
        ai_resp = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_resp = f"AI error: {e}"
    # For convenience, generate TTS for the summary portion (try to extract summary)
    # You may want to parse the AI response; here we put whole ai_resp into TTS
    tts_text = ai_resp if ai_resp else (text[:500] if text else "No text detected.")
    tts_fname = os.path.join(TTS_FOLDER, f"{uuid.uuid4()}.mp3")
    try:
        tts = gTTS(text=tts_text, lang="en")
        tts.save(tts_fname)
        tts_url = f"{request.url_root}tts/{os.path.basename(tts_fname)}"
    except Exception as e:
        tts_url = ""

    return jsonify({
        "ocr_text": text,
        "ai_text": ai_resp,
        "tts_url": tts_url
    })

@app.route("/tts/<filename>", methods=["GET"])
def serve_tts(filename):
    path = os.path.join(TTS_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="audio/mpeg")
    else:
        return "Not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)








