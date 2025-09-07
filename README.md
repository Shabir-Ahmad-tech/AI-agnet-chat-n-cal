# AI-agnet-chat-n-cal

A powerful **Python-based AI assistant** powered by **Google's Gemini AI**.  
It can perform **math calculations**, **automate system tasks**, **manage your to-do list**, **remember preferences**, and even **tell jokes** — with memory that persists across sessions.  

---

## ✨ Features

### 🧮 Mathematical Operations
- Basic arithmetic: addition, subtraction, multiplication, division  
- Advanced: powers, roots, logarithms  
- Trigonometry: sine, cosine, tangent  
- Prime number checking & grade calculation  

### 🗂️ File System Automation
- List, read, write, and create files  
- Create/delete directories  
- Copy files and directories  
- File information: size, creation/modification time  

### 💾 System Information
- Platform details  
- Disk usage  
- Current date & time  

### 📝 Memory & Personalization
- Remembers assistant’s name across sessions  
- Persistent **to-do list** with timestamps  
- Stores & recalls user preferences  
- Data saved & loaded automatically  

### 🎉 Fun Features
- Random jokes  
- Motivational quotes & advice  
- Roll virtual dice  

---

## 🛠️ Installation

### Prerequisites
- Python **3.8+**
- Google Gemini **API key**

### Setup
``` bash
# Clone the repository
git clone <repository-url>
cd ai-assistant
```

### Install dependencies
``` bash
pip install -r requirements.txt
# or install manually
pip install langchain-core langchain-google-genai langgraph python-dotenv
```

Keep your .env safe → never commit API keys.

### 🎯 Extend It
Adding new tools is easy: write a function with @tool, give it a docstring, and add it to the list. The assistant auto-discovers it.

### Create a .env file in the project root:
GOOGLE_API_KEY=your_google_gemini_api_key_here

### Run the Assistant
python ai_assistant.py

## 🚀 Usage

When you start the assistant, you’ll see:

-------- Welcome! Your AI Assistant is ready. Type 'exit' to quit. --------
You can ask me to perform calculations, answer questions, or assist with tasks.
Current assistant name: AI Assistant

## 🔢 Example Commands
### Math:
You: What is 15 multiplied by 27?
Assistant: The product of 15 and 27 is 405.

You: Calculate the square root of 144
Assistant: The square root of 144 is 12.0.


### File Operations:
You: List files in the current directory
Assistant: file1.txt
           file2.py
           notes/
           todo_list.json


### To-Do List:
You: Add "Finish project report" to my to-do list
Assistant: Added 'Finish project report' to your to-do list.


### Personalization:
You: Remember that your name is Jarvis
Assistant: I'll remember that my name is Jarvis for this session.


### Fun:
You: Tell me a joke
Assistant: Why don't scientists trust atoms? Because they make up everything!

## 📁 Project Structure

AI-agnet-chat-n-cal/
│
├── main.py      # Main app
├── .env                 # API keys (ignored in git)
├── todo_list.json       # To-do list storage
├── notes/               # Directory for notes
├── requirements.txt     # Dependencies
└── README.md            # This file


## 🔧 Technical Details
Tools Available
Math Tools: arithmetic, advanced math, trig, prime check
File Tools: create, delete, copy, read/write
System Tools: OS info, disk usage, datetime
Automation: shell commands, timers, organization
Memory: persistent to-do list, preferences, name remembering
Fun Tools: jokes, quotes, dice
Memory System
To-do list stored in todo_list.json
Preferences stored in memory (reset each restart)

## ⚠️ Safety Notes

Shell commands can execute anything → use with caution
File operations can modify/delete data → assistant asks before destructive actions
Keep your .env safe — never commit API keys

## 🎯 Customization

Add new tools by following the pattern:
Create a function with @tool decorator
Add a docstring
Register it in the tools list
The assistant will auto-detect and use it.
## @ 🤝 Contributing

Contributions are welcome!
Report bugs
Suggest new features
Submit PRs with improvements

## Author
**Shabir Ahmad**
