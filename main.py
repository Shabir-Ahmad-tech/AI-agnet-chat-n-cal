from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import math
import time
import datetime
import shutil
import json
import random

load_dotenv()  # Load environment variables from .env file

# =========================================================================
# GLOBAL MEMORY SYSTEM
# This dictionary stores temporary information during the session
# =========================================================================
session_memory = {
    "assistant_name": "Jarvis",  # Default name
    "todo_list": [],                   # To-do items
    "user_preferences": {},            # Any user preferences
    "conversation_history": []         # Store conversation snippets if needed
}

# Helper functions for todo list persistence
def save_todo_list():
    """Saves the to-do list to a file"""
    try:
        with open("todo_list.json", "w") as f:
            json.dump(session_memory["todo_list"], f)
    except Exception as e:
        print(f"Error saving to-do list: {str(e)}")

def load_todo_list():
    """Loads the to-do list from a file"""
    try:
        if os.path.exists("todo_list.json"):
            with open("todo_list.json", "r") as f:
                session_memory["todo_list"] = json.load(f)
            return f"Loaded {len(session_memory['todo_list'])} items from your saved to-do list."
        else:
            return "No saved to-do list found."
    except Exception as e:
        return f"Error loading to-do list: {str(e)}"

# Initialize the Google Generative AI model
def main():
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    # =========================================================================
    # MATH TOOLS SECTION
    # These tools help with various mathematical calculations
    # =========================================================================
    
    @tool
    def add(a: float, b: float) -> float:
        """Adds two numbers."""
        return f"The sum of {a} and {b} is {a + b}."

    @tool
    def subtract(a: float, b: float) -> float:
        """Subtracts two numbers."""
        return f"The difference of {a} and {b} is {a - b}."

    @tool
    def multiply(a: float, b: float) -> float:
        """Multiplies two numbers."""
        return f"The product of {a} and {b} is {a * b}."

    @tool
    def divide(a: float, b: float) -> float:
        """Divides two numbers."""
        if b == 0:
            return "Error: Cannot divide by zero."
        return f"The quotient of {a} and {b} is {a / b}."

    @tool
    def power(base: float, exponent: float) -> float:
        """Calculates the power of a number."""
        return f"The result of {base} raised to the power of {exponent} is {base ** exponent}."

    @tool
    def sqrt(number: float) -> float:
        """Calculates the square root of a number."""
        if number < 0:
            return "Error: Cannot calculate the square root of a negative number."
        return f"The square root of {number} is {math.sqrt(number)}."

    @tool
    def log(number: float, base: float = math.e) -> float:
        """Calculates the logarithm of a number with a given base."""
        if number <= 0:
            return "Error: Cannot calculate the logarithm of a non-positive number."
        return f"The logarithm of {number} with base {base} is {math.log(number, base)}."

    @tool
    def sin(angle: float) -> float:
        """Calculates the sine of an angle in radians."""
        return f"The sine of {angle} is {math.sin(angle)}."

    @tool
    def cos(angle: float) -> float:
        """Calculates the cosine of an angle in radians."""
        return f"The cosine of {angle} is {math.cos(angle)}."

    @tool
    def tan(angle: float) -> float:
        """Calculates the tangent of an angle in radians."""
        return f"The tangent of {angle} is {math.tan(angle)}."

    # =========================================================================
    # GENERAL PURPOSE TOOLS SECTION
    # These tools perform various general tasks
    # =========================================================================
    
    @tool
    def calculate_grade(score: float) -> str:
        """Calculates the letter grade for a given score."""
        if score >= 85:
            return "A1"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "Fail"

    @tool
    def average(numbers: list[float]) -> float:
        """Calculates the average of a list of numbers."""
        return f"The average of {numbers} is {sum(numbers) / len(numbers)}."

    @tool
    def is_prime(number: int) -> bool:
        """Checks if a number is prime."""
        if number < 2:
            return f"{number} is not a prime number."
        if number == 2:
            return f"{number} is a prime number."
        for i in range(2, int(math.sqrt(number)) + 1):
            if number % i == 0:
                return f"{number} is not a prime number."
        return f"{number} is a prime number."

    # =========================================================================
    # FILE SYSTEM AUTOMATION TOOLS SECTION
    # These tools help automate file and directory operations
    # =========================================================================
    
    @tool
    def list_files(directory: str = ".") -> str:
        """Lists all files and directories in a given directory."""
        try:
            return "\n".join(os.listdir(directory))
        except Exception as e:
            return str(e)

    @tool
    def read_file_content(filepath: str) -> str:
        """Reads the content of a file."""
        try:
            with open(filepath, "r") as f:
                return f.read()
        except Exception as e:
            return str(e)

    @tool
    def write_file_content(filepath: str, content: str) -> str:
        """Writes content to a file."""
        try:
            with open(filepath, "w") as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return str(e)

    @tool
    def create_directory(directory_path: str) -> str:
        """Creates a new directory at the specified path."""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return f"Directory created successfully at {directory_path}"
        except Exception as e:
            return f"Error creating directory: {str(e)}"

    @tool
    def delete_file_or_directory(path: str) -> str:
        """Deletes a file or directory at the specified path."""
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"File deleted: {path}"
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return f"Directory deleted: {path}"
            else:
                return f"Path not found: {path}"
        except Exception as e:
            return f"Error deleting: {str(e)}"

    @tool
    def copy_file_or_directory(source: str, destination: str) -> str:
        """Copies a file or directory from source to destination."""
        try:
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                return f"File copied from {source} to {destination}"
            elif os.path.isdir(source):
                shutil.copytree(source, destination)
                return f"Directory copied from {source} to {destination}"
            else:
                return f"Source not found: {source}"
        except Exception as e:
            return f"Error copying: {str(e)}"

    @tool
    def get_file_info(filepath: str) -> str:
        """Gets information about a file (size, creation time, modification time)."""
        try:
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
            
            stat_info = os.stat(filepath)
            size = stat_info.st_size
            created = datetime.datetime.fromtimestamp(stat_info.st_ctime)
            modified = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            
            return f"File: {filepath}\nSize: {size} bytes\nCreated: {created}\nModified: {modified}"
        except Exception as e:
            return f"Error getting file info: {str(e)}"

    # =========================================================================
    # SYSTEM INFORMATION TOOLS SECTION
    # These tools provide information about the system
    # =========================================================================
    
    @tool
    def get_system_info() -> str:
        """Gets basic system information (platform, processor, etc.)."""
        try:
            platform_info = os.uname()
            return f"System: {platform_info.sysname}\nNode: {platform_info.nodename}\nRelease: {platform_info.release}\nVersion: {platform_info.version}\nMachine: {platform_info.machine}"
        except:
            return f"Platform: {os.name}\nSystem info not available on this platform"

    @tool
    def get_disk_usage() -> str:
        """Gets disk usage information."""
        try:
            disk_usage = shutil.disk_usage("/")
            return f"Total: {disk_usage.total // (2**30)} GB\nUsed: {disk_usage.used // (2**30)} GB\nFree: {disk_usage.free // (2**30)} GB"
        except Exception as e:
            return f"Error getting disk usage: {str(e)}"

    @tool
    def get_current_datetime() -> str:
        """Gets the current date and time."""
        now = datetime.datetime.now()
        return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    # =========================================================================
    # PROCESS AUTOMATION TOOLS SECTION
    # These tools help automate various processes
    # =========================================================================
    
    @tool
    def run_shell_command(command: str) -> str:
        """
        Executes a shell command.
        WARNING: This tool can execute any shell command and can be dangerous. Use with extreme caution.
        """
        try:
            return os.popen(command).read()
        except Exception as e:
            return str(e)

    @tool
    def countdown_timer(seconds: int) -> str:
        """Starts a countdown timer for the specified number of seconds."""
        try:
            for i in range(seconds, 0, -1):
                print(f"\rTime remaining: {i} seconds", end="")
                time.sleep(1)
            print("\rCountdown finished!          ")
            return "Countdown completed successfully"
        except Exception as e:
            return f"Error with timer: {str(e)}"

    @tool
    def create_notes_file(filename: str, content: str) -> str:
        """Creates a notes file with the given content in a notes directory."""
        try:
            # Create notes directory if it doesn't exist
            notes_dir = "notes"
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir)
            
            # Create the file
            filepath = os.path.join(notes_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            
            return f"Notes file created successfully at {filepath}"
        except Exception as e:
            return f"Error creating notes file: {str(e)}"

    @tool
    def organize_files_by_extension(directory: str = ".") -> str:
        """Organizes files in a directory into folders based on their extensions."""
        try:
            # Get all files in the directory
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            
            # Create folders for each file extension and move files
            for file in files:
                file_ext = os.path.splitext(file)[1][1:]  # Get extension without dot
                if not file_ext:
                    file_ext = "no_extension"
                
                # Create folder if it doesn't exist
                ext_folder = os.path.join(directory, file_ext)
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder)
                
                # Move file to the folder
                src = os.path.join(directory, file)
                dest = os.path.join(ext_folder, file)
                shutil.move(src, dest)
            
            return f"Organized {len(files)} files by extension in {directory}"
        except Exception as e:
            return f"Error organizing files: {str(e)}"

    # =========================================================================
    # MEMORY AND PERSONALIZATION TOOLS
    # These tools help the assistant remember things about the user
    # =========================================================================
    
    @tool
    def remember_name(name: str) -> str:
        """Remembers the assistant's name for this session."""
        global session_memory
        session_memory["assistant_name"] = name
        return f"I'll remember that my name is {name} for this session."

    @tool
    def get_remembered_name() -> str:
        """Retrieves the name the user wants to call the assistant."""
        global session_memory
        return f"You asked me to remember that my name is {session_memory['assistant_name']}."

    @tool
    def add_todo_item(task: str) -> str:
        """Adds an item to the to-do list."""
        global session_memory
        # Add timestamp to the task
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        session_memory["todo_list"].append({"task": task, "added": timestamp, "completed": False})
        
        # Also save to file for persistence
        save_todo_list()
        
        return f"Added '{task}' to your to-do list. You now have {len(session_memory['todo_list'])} items."

    @tool
    def show_todo_list() -> str:
        """Shows all items in the to-do list."""
        global session_memory
        if not session_memory["todo_list"]:
            return "Your to-do list is empty!"
        
        result = "Your To-Do List:\n"
        for i, item in enumerate(session_memory["todo_list"], 1):
            status = "✓" if item["completed"] else "☐"
            result += f"{i}. {status} {item['task']} (added: {item['added']})\n"
        
        return result

    @tool
    def complete_todo_item(item_number: int) -> str:
        """Marks a to-do item as completed."""
        global session_memory
        if item_number < 1 or item_number > len(session_memory["todo_list"]):
            return f"Invalid item number. Please choose between 1 and {len(session_memory['todo_list'])}."
        
        session_memory["todo_list"][item_number-1]["completed"] = True
        completed_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        session_memory["todo_list"][item_number-1]["completed_at"] = completed_time
        
        # Save to file
        save_todo_list()
        
        task = session_memory["todo_list"][item_number-1]["task"]
        return f"Marked '{task}' as completed at {completed_time}."

    @tool
    def delete_todo_item(item_number: int) -> str:
        """Deletes an item from the to-do list."""
        global session_memory
        if item_number < 1 or item_number > len(session_memory["todo_list"]):
            return f"Invalid item number. Please choose between 1 and {len(session_memory['todo_list'])}."
        
        removed_task = session_memory["todo_list"].pop(item_number-1)
        
        # Save to file
        save_todo_list()
        
        return f"Removed '{removed_task['task']}' from your to-do list."

    @tool
    def clear_todo_list() -> str:
        """Clears all items from the to-do list."""
        global session_memory
        count = len(session_memory["todo_list"])
        session_memory["todo_list"] = []
        
        # Delete the todo file
        if os.path.exists("todo_list.json"):
            os.remove("todo_list.json")
        
        return f"Cleared all {count} items from your to-do list."

    @tool
    def save_todo_list_tool() -> str:
        """Saves the to-do list to a file (manually triggered)."""
        save_todo_list()
        return "To-do list saved to file."

    @tool
    def load_todo_list_tool() -> str:
        """Loads the to-do list from a file (manually triggered)."""
        return load_todo_list()

    @tool
    def remember_preference(key: str, value: str) -> str:
        """Remembers a user preference for this session."""
        global session_memory
        session_memory["user_preferences"][key] = value
        return f"I'll remember that you prefer {key} = {value}."

    @tool
    def get_preference(key: str) -> str:
        """Retrieves a remembered user preference."""
        global session_memory
        if key in session_memory["user_preferences"]:
            return f"You prefer {key} = {session_memory['user_preferences'][key]}."
        else:
            return f"I don't remember any preference for {key}."

    # =========================================================================
    # COOL AUTOMATION TOOLS
    # These tools do something fun or interesting
    # =========================================================================
    
    @tool
    def tell_joke() -> str:
        """Tells a random joke."""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "How does a penguin build its house? Igloos it together!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        return random.choice(jokes)

    @tool
    def random_advice() -> str:
        """Gives random advice."""
        advice_list = [
            "Take breaks when working long hours. Your productivity will thank you.",
            "Drink more water! It's good for your health and concentration.",
            "Don't forget to back up your important files regularly.",
            "A 5-minute walk outside can refresh your mind more than you think.",
            "Learn something new every day, even if it's small."
        ]
        return random.choice(advice_list)

    @tool
    def motivational_quote() -> str:
        """Shares a motivational quote."""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "It always seems impossible until it's done. - Nelson Mandela",
            "Don't count the days, make the days count. - Muhammad Ali",
            "Quality is not an act, it is a habit. - Aristotle",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
        ]
        return random.choice(quotes)

    @tool
    def roll_dice(sides: int = 6) -> str:
        """Rolls a dice with the specified number of sides."""
        result = random.randint(1, sides)
        return f"You rolled a {result} on a {sides}-sided die!"

    # =========================================================================
    # TOOLS LIST
    # Add all tools to this list so the agent can use them
    # =========================================================================
    
    tools = [
        # Math tools
        add, subtract, multiply, divide, power, sqrt, log, sin, cos, tan,
        # General purpose tools
        calculate_grade, average, is_prime,
        # File system automation tools
        list_files, read_file_content, write_file_content, create_directory,
        delete_file_or_directory, copy_file_or_directory, get_file_info,
        # System information tools
        get_system_info, get_disk_usage, get_current_datetime,
        # Process automation tools
        run_shell_command, countdown_timer, create_notes_file, organize_files_by_extension,
        # Memory and personalization tools
        remember_name, get_remembered_name, add_todo_item, show_todo_list,
        complete_todo_item, delete_todo_item, clear_todo_list, save_todo_list_tool,
        load_todo_list_tool, remember_preference, get_preference,
        # Cool tools
        tell_joke, random_advice, motivational_quote, roll_dice
    ]

    # Create the agent with all the tools
    agent_executor = create_react_agent(model, tools)

    # =========================================================================
    # LOAD SAVED DATA AT STARTUP
    # =========================================================================
    
    # Load any saved to-do list
    load_result = load_todo_list()
    print(load_result)

    # =========================================================================
    # MAIN INTERFACE LOOP
    # This is where the program interacts with the user
    # =========================================================================
    
    print("--------Welcome! Your AI Assistant is ready. Type 'exit' to quit.--------")
    print("You can ask me to perform calculations, answer questions, or assist with various tasks.")
    print("I can remember your preferences, manage a to-do list, and even tell jokes!")
    print(f"Current assistant name: {session_memory['assistant_name']}")

    while True:
        user_input = input("\nYou: ").strip()  # Get user input and remove leading/trailing whitespace

        if user_input.lower() == 'exit':
            # Save todo list before exiting
            save_todo_list()
            print("Exiting the program. Goodbye!")
            break

        print("\nAssistant: ", end="")

        # Stream the response from the agent executor
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            # Print the assistant's response as it streams in
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

        print()  # Add a newline after the assistant's full response.

if __name__ == "__main__":
    main()