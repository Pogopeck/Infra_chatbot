import google.generativeai as genai
genai.configure(api_key="AIzaSyBE7W5QfYkIEYnEMCO_NVOHES2hNB3qL3Y")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)