from google import genai

client = genai.Client(api_key="AIzaSyCqD_qQcLw3ipgyqLL2Ef7dEO7qlSsGqGA")

response = client.models.generate_content(
    model="gemini-1.0-pro",
    contents="Extract skills from: Python developer with SQL, pandas and 0-1 years experience"
)

print(response.text)