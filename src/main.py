import os
import traceback
from dotenv import load_dotenv
from agents.infra_agent import get_terraform_generator, extract_terraform_code
from utils.terraform_runner import run_terraform_plan

# Load environment
load_dotenv()

def main():
    # Safety check
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: GOOGLE_API_KEY not found in .env")
        return

    print("🚀 AI Infrastructure Chatbot (Gemini 2.0 + Terraform)")
    print("💡 Describe your AWS infra in plain English (e.g., 'Create an S3 bucket')\n")
    
    try:
        user_input = input("💬 Your request: ").strip()
        if not user_input:
            print("⚠️ No input provided. Exiting.")
            return

        print("\n🧠 Generating Terraform code...\n")
        chain = get_terraform_generator()
        raw_response = chain.invoke({"input": user_input})
        
        tf_code = extract_terraform_code(raw_response)
        if not tf_code or len(tf_code) < 20:
            print("❌ Failed to generate valid Terraform code.")
            print("Raw LLM output:", repr(raw_response[:200]))
            return

        print("📄 Generated Terraform:\n")
        print(tf_code)

        print("\n🔍 Running `terraform plan` (dry-run only)...\n")
        plan_output = run_terraform_plan(tf_code)
        print(plan_output)

    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()