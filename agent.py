import hashlib
import os
import subprocess
from smolagents import CodeAgent, HfApiModel

model_id = 'https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud/' 
model = HfApiModel(model_id=model_id, token="...")

agent = CodeAgent(tools=[], model=model, add_base_tools=True, additional_authorized_imports=["requests","json", "pytest", "uuid"])
test_storage = ''

def get_file_hash(content):
    """Generate a hash for the file content."""
    return hashlib.md5(content.encode()).hexdigest()

# Read manual steps from file
with open("manual_steps.txt", "r") as manual_steps_file:
    manual_steps = manual_steps_file.read()

current_hash = get_file_hash(manual_steps)
previous_hash = ""

# Check if hash file exists and read previous hash
if os.path.exists("manual_steps_hash.txt"):
    with open("manual_steps_hash.txt", "r") as hash_file:
        previous_hash = hash_file.read().strip()

if os.path.exists("test_storage.py") and current_hash == previous_hash:
    # Manual steps haven't changed, run existing tests
    print("Manual steps unchanged. Running existing tests...")
    result = subprocess.run(["pytest", "test_storage.py", "-v"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Tests passed successfully!")
    else:
        print("Tests failed! Analyzing failures...")
        # Use the agent to analyze test failures
        analysis_prompt = f"""
        The following tests have failed:
        
        {result.stdout}
        {result.stderr}
        
        Analyze why these tests are failing and suggest fixes:
        apply fixes and return the updated test code in the format of pytest tests, make sure each test is a separate function, make sure syntax is correct
        """
        test_storage = agent.run(analysis_prompt)
else:
    # Manual steps have changed or test file doesn't exist, update tests
    print("Manual steps have changed or tests don't exist. Generating new tests...")
    prompt = f"""
    Pre-requisites: use pytest for testing and requests for making API calls. I want to see the logs from api calls
    Write automated tests for the following test steps:
    {manual_steps}
    - run the tests created by the agent using http://127.0.0.1:8000/users as the base url and make sure the tests pass
    - then return generated python code in the format of pytest tests, make sure each test is a separate function, make sure syntax is correct"""
    
    test_storage = agent.run(prompt)
    
    # Write the test_storage to a file
    with open("test_storage.py", "w") as file:
        file.write(test_storage)
    
    # Save the new hash
    with open("manual_steps_hash.txt", "w") as hash_file:
        hash_file.write(current_hash)
    
    print("New tests have been generated and saved to test_storage.py")
    
    # Run the new tests
    print("Running new tests...")
    result = subprocess.run(["pytest", "test_storage.py", "-v"], capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print("New tests failed! Please check the output above.")