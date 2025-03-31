from flask import Flask, render_template, request, jsonify
import openai
import elevenlabs
import os
from dotenv import load_dotenv

load_dotenv()  # .env फाइल से variables लोड करेगा

app = Flask(__name__)

# APIs कॉन्फ़िगर करें
openai.api_key = os.getenv("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")
elevenlabs.set_api_key(os.getenv("ELEVENLABS_KEY"))

# नमूना डेटाबेस
DEAD_DB = {
    "grandfather": {
        "bio": "एक दयालु व्यक्ति जिन्होंने 1947 में भारत की आजादी देखी",
        "voice_id": "ABCDEFG123"  # ElevenLabs वॉइस आईडी
    }
}

@app.route("/")
def home():
    return render_template("index.html", persons=DEAD_DB.keys())

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    person = data["person"]
    message = data["message"]
    
    # AI को प्रॉम्प्ट भेजें
    prompt = f"""You are {person}. {DEAD_DB[person]['bio']}.
    Respond in Hindi/English mix as if you were alive:
    {message}"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
    
    return jsonify({
        "text": response,
        "audio": None  # ElevenLabs इंटीग्रेशन के लिए आपको API key चाहिए
    })

if __name__ == "__main__":
    app.run(debug=True)
