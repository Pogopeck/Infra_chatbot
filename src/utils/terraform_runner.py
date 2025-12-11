import os
import tempfile
import subprocess

def run_terraform_plan(terraform_code: str) -> str:
    """
    Safely run `terraform init` and `terraform plan` in an isolated temp directory.
    NEVER runs `apply`. Times out after 30 seconds for safety.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tf_path = os.path.join(tmpdir, "main.tf")
        with open(tf_path, "w") as f:
            f.write(terraform_code)
        
        try:
            # Initialize
            init_result = subprocess.run(
                ["terraform", "init", "-input=false"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=20
            )
            if init_result.returncode != 0:
                return f"❌ Terraform init failed:\n{init_result.stderr}"

            # Plan
            plan_result = subprocess.run(
                ["terraform", "plan", "-input=false", "-no-color"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30
            )
            if plan_result.returncode == 0:
                return f"✅ Plan succeeded:\n{plan_result.stdout}"
            else:
                return f"⚠️ Plan failed (code may still be valid):\n{plan_result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "⏰ Terraform command timed out (safety cutoff)."
        except Exception as e:
            return f"💥 Unexpected error: {str(e)}"