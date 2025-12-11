from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.infra_agent import get_terraform_generator, extract_terraform_code
from src.utils.terraform_runner import run_terraform_plan
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

load_dotenv()

# Safety check
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY missing in environment")

app = FastAPI(
    title="AI Infrastructure Chatbot",
    description="Convert natural language to Terraform using Google Gemini",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Visit /static/index.html for UI"}

class InfraRequest(BaseModel):
    query: str

class InfraResponse(BaseModel):
    terraform_code: str
    plan_output: str

@app.post("/generate", response_model=InfraResponse)
async def generate_terraform(request: InfraRequest):
    try:
        # Generate code
        chain = get_terraform_generator()
        raw = chain.invoke({"input": request.query})
        tf_code = extract_terraform_code(raw)
        
        if not tf_code or len(tf_code) < 20:
            raise HTTPException(status_code=400, detail="Failed to generate valid Terraform")
        
        # Run plan
        plan_output = run_terraform_plan(tf_code)
        
        return InfraResponse(
            terraform_code=tf_code,
            plan_output=plan_output
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")