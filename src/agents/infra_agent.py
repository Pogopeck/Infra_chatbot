import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_terraform_generator():
    """
    Returns a LangChain chain that converts natural language into valid Terraform code
    using Google Gemini 2.0 Flash (confirmed available in your Google project).
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.05,
        max_output_tokens=1024,
        convert_system_message_to_human=True
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are an expert AWS infrastructure engineer. Generate ONLY raw Terraform code using the AWS provider.
Rules:
- NEVER wrap code in ``` or any markdown.
- NEVER explain or add comments.
- Include required_providers and provider blocks.
- Use AWS provider "~> 5.0".
- Tag all resources with Name = "<descriptive>".
- Use realistic CIDRs and AZs (e.g., us-east-1a).
- Assume region is specified or default to us-east-1.
"""),
        ("human", "{input}")
    ])
    
    return prompt | llm | StrOutputParser()


def extract_terraform_code(text: str) -> str:
    """
    Remove any Markdown code fences (```terraform, ```hcl, etc.) and return clean HCL.
    """
    match = re.search(r"```(?:terraform|hcl|tf)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()