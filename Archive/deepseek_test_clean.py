import requests

print("🚀 Script started")

url = "http://127.0.0.1:1234/v1/chat/completions"

payload = {
    "model": "meta-llama/meta-llama-3-8b-instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I survive my first night in Minecraft?"}
    ],
    "temperature": 0.7
}


try:
    print("⏳ Sending request to DeepSeek...")
    response = requests.post(url, json=payload)
    print(f"📡 Status Code: {response.status_code}")
    print("🧾 Raw Response:", response.text)
    response.raise_for_status()
    print("✅ Final Answer:")
    print(response.json()["choices"][0]["message"]["content"])
except Exception as e:
    print("❌ DeepSeek test failed:", e)
