# Multi-Agent Systems with LangChain and Local LLMs

A collection of three advanced multi-agent systems demonstrating different patterns of agent collaboration using Python, LangChain, and local language models (Ollama).

## 🤖 Implemented Systems

### 1. Software Development Team
A collaborative coding system with three specialized agents:
- **Manager Agent**: Breaks down feature requests into actionable tasks
- **Coder Agent**: Implements the code based on tasks
- **Reviewer Agent**: Reviews code quality and sends feedback

**Pattern**: Sequential workflow with feedback loops

### 2. Red Teaming / Vibe Hacking Bot
An adversarial system for testing AI safety:
- **Attacker Agent**: Attempts to bypass safety guardrails using creative techniques
- **Defender Agent**: Analyzes attacks and suggests security patches
- **Target Agent**: The AI system being tested

**Pattern**: Adversarial interaction with iterative hardening

### 3. Autonomous Social Media Manager
An end-to-end content creation pipeline:
- **Trend Monitor**: Identifies relevant trending topics
- **Content Creator**: Writes engaging captions
- **Image Describer**: Creates prompts for image generation (DALL-E/Midjourney)
- **Brand Guardian**: Ensures brand consistency
- **Scheduler**: Determines optimal posting times

**Pattern**: Multi-stage pipeline with quality gates

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
   - Download from: https://ollama.ai
   - Install a model: `ollama pull llama2` (or llama3, mistral, etc.)

## 🚀 Quick Start

### 1. Clone or navigate to the project directory
```bash
cd d:\personal\Multi-Agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment (optional)
```bash
copy .env.example .env
# Edit .env to customize Ollama settings if needed
```

### 6. Verify Ollama is running
```bash
ollama list
# Should show your installed models (e.g., llama2)
```

### 7. Run the interactive demo
```bash
python main.py
```

## 📁 Project Structure

```
Multi-Agent/
│
├── main.py                      # Interactive demo runner
├── software_dev_team.py         # Software development team system
├── red_teaming_bot.py           # Red teaming/adversarial system
├── social_media_manager.py      # Social media automation system
│
├── config.py                    # Configuration and settings
├── utils.py                     # Utility functions
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment configuration
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🎮 Usage Examples

### Running Individual Systems

#### Software Development Team
```bash
python software_dev_team.py
```
Example: "Create a Python function for binary search with error handling"

#### Red Teaming Bot
```bash
python red_teaming_bot.py
```
Tests AI safety guardrails through adversarial prompting

#### Social Media Manager
```bash
python social_media_manager.py
```
Creates complete social media posts with trend analysis

### Using the Interactive Demo
```bash
python main.py
```
Choose from the menu to run any system with custom inputs.

## ⚙️ Configuration

Edit [.env](.env) to customize:

```env
OLLAMA_BASE_URL=http://localhost:11434  # Ollama server URL
OLLAMA_MODEL=llama2                      # Model to use (llama2, llama3, mistral, etc.)
```

Temperature settings in [config.py](config.py):
- `TEMPERATURE_CREATIVE = 0.8` - For creative tasks
- `TEMPERATURE_ANALYTICAL = 0.3` - For code/analytical tasks
- `TEMPERATURE_BALANCED = 0.5` - For balanced tasks

## 🔧 Customization

### Adding New Agents

Each system follows a simple agent pattern:

```python
class MyAgent:
    def __init__(self):
        self.llm = Ollama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=0.7
        )
        self.prompt = PromptTemplate(...)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def perform_action(self, input_data):
        result = self.chain.run(input=input_data)
        return result
```

### Using Different Models

Install alternative models:
```bash
ollama pull llama3
ollama pull mistral
ollama pull codellama
```

Update `.env`:
```env
OLLAMA_MODEL=llama3  # or mistral, codellama, etc.
```

## 📊 System Workflows

### Software Dev Team Flow
```
User Request → Manager (tasks) → Coder (code) → Reviewer (feedback) → ✓ Done
                                      ↑                    |
                                      └────── (if issues) ─┘
```

### Red Teaming Flow
```
Objective → Attacker (prompt) → Target (response) → Defender (analysis) → Patch
                ↑                                                           |
                └──────────────── (iterate with patches) ──────────────────┘
```

### Social Media Flow
```
Industry → Trends → Content → Brand Check → Image Prompt → Schedule → ✓ Post Ready
                       ↑           |
                       └─ (revise) ┘
```

## 🐛 Troubleshooting

**Ollama connection error:**
- Ensure Ollama is running: `ollama serve`
- Check the base URL in `.env` matches your Ollama instance

**Model not found:**
- Install the model: `ollama pull llama2`
- Verify with: `ollama list`

**Slow performance:**
- Use a smaller model: `ollama pull phi`
- Reduce temperature settings
- Limit max_iterations in the code

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## 🎯 Next Steps

**Enhancements you can add:**

1. **Persistent Memory**: Add vector databases (Chroma, Pinecone) for agent memory
2. **Real API Integration**: Connect to actual DALL-E, Twitter API, etc.
3. **Web Interface**: Build a Streamlit or Gradio UI
4. **More Agents**: Add QA tester, DevOps agent, etc.
5. **Advanced Orchestration**: Use LangGraph for complex workflows
6. **Logging & Analytics**: Track agent performance and costs

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Models](https://ollama.ai/library)
- [Multi-Agent Systems Patterns](https://github.com/langchain-ai/langchain)

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to extend these systems and add your own multi-agent patterns!

---

**Built with ❤️ using LangChain and Ollama**
