import os
import subprocess
from phi.model.ollama import Ollama
from phi.model.openai import OpenAIChat
from phi.model.google import Gemini

from phi.agent import Agent

# os.environ["OPENAI_API_KEY"] = "AAA"
os.environ["GOOGLE_API_KEY"] = "AAA"

current_dir = "C:\\Project\\Python\\phidata_practice\\ai_agent"
java_file_name: str = "Calculator.java"
test_file_name: str= "CalculatorTest.java"
java_file_path = f"{current_dir}\\{java_file_name}"
test_file_path = f"{current_dir}\\{test_file_name}"
class_name: str = "CalculatorTest"

def read_my_java_file() -> str:
    """Reads the java file and returns the content as a string."""
    with open(java_file_path, 'r') as file:
        return file.read()

def write_code_to_file(java_code: str):
    """Writes the java code to a file."""
    with open(test_file_path, 'w') as file:
        file.write(java_code)

def compile_java_code():
    """Compiles the java code and returns the output."""
    result = subprocess.run(['javac', '-cp', f'{current_dir}\\*', java_file_path, test_file_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Compilation failed: {result.stderr}")

def run_unittest():
    """Runs the unittest and returns the output."""
    result = subprocess.run(['java', '-cp', f"{current_dir}\\*;{current_dir}", "org.junit.runner.JUnitCore", f'{class_name}'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Execution failed: {result.stderr}")
    with open(f"{current_dir}\\unitTest_output.txt", 'w') as file:
        file.write(result.stdout)
    return result.stdout

javacode = read_my_java_file()

# agent = Agent(model=Ollama(id="llama3.2:1b"), tools=[read_my_java_file ,write_code_to_file, compile_java_code, run_unittest], show_tool_calls=True, markdown=True)
# agent = Agent(model=OpenAIChat(id="gpt-4o-mini") ,tools=[read_my_java_file ,write_code_to_file, compile_java_code, run_unittest], show_tool_calls=True, markdown=True)
agent = Agent(model=Gemini(id="gemini-1.5-flash") ,
              description="You are a AI Agent of a java developer",
              instructions=["Please use our tools to generate a Junit code and then compile and run it successfully."],
              tools=[write_code_to_file, compile_java_code, run_unittest], 
              show_tool_calls=True, 
              markdown=True)

prompt = f"the target java class as follows: \n\n{javacode}"
agent.print_response(message=prompt, stream=True, show_full_reasoning=True)
# print(read_my_java_file())
# compile_java_code()
# print(run_unittest())