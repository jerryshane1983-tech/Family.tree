import subprocess
import json
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

def main():
    # Simple JSON-RPC style interface for the MCP
    # This is a basic version that the AI can call via the CLI
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        
        try:
            request = json.loads(line)
            tool = request.get("method")
            params = request.get("params", {})
            
            if tool == "sherlock":
                username = params.get("username")
                # Use the local installation of Sherlock in Termux
                sherlock_path = "/data/data/com.termux/files/home/sherlock-tool"
                output = run_command(f"PYTHONPATH={sherlock_path} python3 -m sherlock_project {username} --timeout 10 --print-found")
                print(json.dumps({"result": output}))
                
            elif tool == "holehe":
                email = params.get("email")
                output = run_command(f"holehe {email}")
                print(json.dumps({"result": output}))
                
            elif tool == "harvester":
                domain = params.get("domain")
                output = run_command(f"theHarvester -d {domain} -l 100 -b google")
                print(json.dumps({"result": output}))
                
            else:
                print(json.dumps({"error": "Unknown tool"}))
                
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
