import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

# Load data from database/tribun_detail.json
with open("database/tribun_detail.json", "r", encoding="utf-8") as file:
    tribun_data = json.load(file)

# Prepare the results list
results = []

# Iterate over each content in tribun_data
if isinstance(tribun_data, list):
    for item in tribun_data:
        prompt = item.get("content", "")
        if prompt:  # Ensure the prompt is not empty
            # Request for solution
            solution = requests.post(OLLAMA_URL, json={
                "model": "llama3.2",
                "prompt": f"Ringkas dan Berikan solusi secara singkat saja untuk berita berikut  :\n\n{prompt}",
                "stream": False
            })
            solution_data = solution.json()
            solution = solution_data.get("response", "")

            category = requests.post(OLLAMA_URL, json={
                "model": "llama3.2",
                "prompt": f" Tentukan kategori berita ini. Pilih salah satu dari kategori berikut: hukum, kriminal, politik, ekonomi, teknologi, pendidikan, hiburan, agama. Hanya sebutkan kategori yang sesuai tanpa penjelasan. :\n\n {prompt}",
                "stream": False
            })
            category_data = category.json()
            category = category_data.get("response", "")

            # Append the results
            results.append({
                "content": prompt,
                "summary and solution": solution,
                "category": category
            })

# Save the results to a JSON file
with open("database/hasil_analisis.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Analysis completed and saved to database/hasil_analisis.json")