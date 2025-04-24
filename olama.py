import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

prompt = """
Berikut adalah isi berita:

"Pemerintah Indonesia mengumumkan kebijakan baru terkait pajak untuk sektor digital..."

Tolong:
1. Identifikasi topik utama.
2. Tentukan sentimen (positif, negatif, netral).
3. Buat ringkasan singkat dalam 2-3 kalimat.
"""

response = requests.post(OLLAMA_URL, json={
    "model": "llama3.2",
    "prompt": prompt,
    "stream": False
})

data = response.json()

# Tampilkan dan simpan sebagai file JSON
print(data["response"])

with open("database/hasil_analisis.json", "w", encoding="utf-8") as f:
    import json
    json.dump({"analysis": data["response"]}, f, ensure_ascii=False, indent=4)