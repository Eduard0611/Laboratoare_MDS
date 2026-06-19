import json
from datetime import datetime
from openai import OpenAI
import re

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Our simple in-memory database
tasks = {}
task_id_counter = 1

# Tool Implementations
def add_task(description, due_date="None"):
    global task_id_counter
    # Formatăm "None" dacă primim null din JSON
    if not due_date:
        due_date = "None"
    tasks[task_id_counter] = {"description": description, "due_date": due_date, "done": False}
    task_id_counter += 1
    return f"Success: Task {task_id_counter - 1} created."

def list_tasks():
    if not tasks:
        return "List is empty."
    
    output = []
    for tid, task in tasks.items():
        status = "[x]" if task["done"] else "[ ]"
        date_str = f" ({task['due_date']})" if task["due_date"] != "None" else ""
        output.append(f"{status} {tid}: {task['description']}{date_str}")
    return "\n".join(output)

def mark_done(task_id):
    try:
        tid = int(task_id)
        if tid in tasks:
            tasks[tid]["done"] = True
            return f"Success: Task {tid} marked as solved."
        return f"Error: Task {tid} not found."
    except (ValueError, TypeError):
        return f"Error: Invalid task ID '{task_id}'."

def delete_task(task_id):
    try:
        tid = int(task_id)
        if tid in tasks:
            del tasks[tid]
            return f"Success: Task {tid} deleted."
        return f"Error: Task {tid} not found."
    except (ValueError, TypeError):
         return f"Error: Invalid task ID '{task_id}'."

# Define the tools for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Description of the task"},
                    "due_date": {"type": "string", "description": "Due date if specified (e.g. May 25, 2026), else 'None'"}
                },
                "required": ["description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all current tasks.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mark_done",
            "description": "Mark a specific task as done.",
            "parameters": {
                "type": "object",
                "properties": {"task_id": {"type": "integer", "description": "The ID of the task"}},
                "required": ["task_id"],
            },
        },
    },
     {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a specific task.",
            "parameters": {
                "type": "object",
                "properties": {"task_id": {"type": "integer", "description": "The ID of the task"}},
                "required": ["task_id"],
            },
        },
    }
]

def execute_local_tools(calls_list):
    """Execută o listă de apeluri de funcții și returnează rezultatele formatate."""
    tool_results = []
    for call in calls_list:
        name = call.get("name")
        args = call.get("arguments", {})
        
        if name == "add_task":
            result = add_task(args.get("description"), args.get("due_date", "None"))
        elif name == "list_tasks":
            result = list_tasks()
        elif name == "mark_done":
            result = mark_done(args.get("task_id"))
        elif name == "delete_task":
            result = delete_task(args.get("task_id"))
        else:
            result = "Unknown tool."
        tool_results.append(result)
    return tool_results

def run_agent(user_input, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="mistral",
        messages=conversation_history,
        tools=tools
    )
    
    msg = response.choices[0].message
    
    # 1. Cazul Ideal: Modelul folosește corect API-ul de tool_calls [cite: 597, 599]
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        conversation_history.append(msg)
        
        calls_list = []
        for tc in msg.tool_calls:
            calls_list.append({
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments)
            })
            
        results = execute_local_tools(calls_list)
        
        # Adăugăm rezultatele în istoric (necesar pentru API-ul OpenAI)
        for tc, res in zip(msg.tool_calls, results):
             conversation_history.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": res
            })
             
        # Pentru un output curat, exact ca in cerinta
        return "\n".join(results)

    # 2. Cazul Fallback: Modelul returnează JSON-ul ca text simplu [cite: 621]
    elif msg.content:
        # Căutăm orice arată a listă JSON (care începe cu '[' și se termină cu ']')
        match = re.search(r'\[\s*\{.*\}\s*\]', msg.content, re.DOTALL)
        if match:
            try:
                json_str = match.group(0)
                calls_list = json.loads(json_str)
                
                conversation_history.append({"role": "assistant", "content": msg.content})
                results = execute_local_tools(calls_list)
                
                for call, res in zip(calls_list, results):
                     conversation_history.append({"role": "system", "content": f"Tool '{call.get('name')}' returned: {res}"})
                
                return "\n".join(results)
            except Exception as e:
                pass # Dacă nu e JSON valid, trecem mai departe și îl tratăm ca text
                
        # Niciun JSON valid găsit, tratăm ca mesaj normal
        conversation_history.append({"role": "assistant", "content": msg.content})
        return msg.content
        
    return "No response from model."

if __name__ == "__main__":
    current_date = datetime.now().strftime("%B %d, %Y")
    print(f"TODO Agent Active. ({current_date})\n")
    
    system_prompt = f"You are a strict task manager agent. Today is {current_date}. Only use the provided tools to manage tasks. NEVER write JSON in plain text. Always use the native tool calling mechanism. Do not add conversational filler."
    history = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            output = run_agent(user_input, history)
            print(f"AI: {output}\n")
        except KeyboardInterrupt:
            break