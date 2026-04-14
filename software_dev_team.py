"""
Software Development Team Multi-Agent System
============================================
This system simulates a software development team with three agents:
- Manager: Breaks down feature requests into tasks
- Coder: Implements the code
- Reviewer: Tests and reviews the code, sends feedback
"""

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from colorama import Fore
import config
from utils import print_agent_message, print_section


class ManagerAgent:
    """Agent responsible for breaking down feature requests into tasks."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_ANALYTICAL
        )
        
        self.prompt = PromptTemplate(
            input_variables=["feature_request"],
            template="""You are a Software Development Manager. Your job is to break down feature requests into clear, actionable tasks.

Feature Request: {feature_request}

Break this down into 3-5 specific tasks. For each task, provide:
1. Task number
2. Clear description
3. Estimated complexity (Low/Medium/High)

Format your response as a numbered list. Be concise and specific."""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def create_tasks(self, feature_request: str) -> str:
        """Break down a feature request into tasks."""
        print_agent_message("Manager Agent", 
                          f"Analyzing feature request: {feature_request}", 
                          Fore.MAGENTA)
        
        tasks = self.chain.run(feature_request=feature_request)
        print_agent_message("Manager Agent", f"Tasks created:\n{tasks}", Fore.MAGENTA)
        return tasks


class CoderAgent:
    """Agent responsible for writing code."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_ANALYTICAL
        )
        
        self.prompt = PromptTemplate(
            input_variables=["tasks", "feedback"],
            template="""You are an Expert Software Developer. You write clean, well-documented Python code.

Tasks to implement:
{tasks}

{feedback}

Write Python code to implement these tasks. Include:
1. Proper function/class structure
2. Docstrings
3. Error handling
4. Comments for complex logic

Provide ONLY the code, well-formatted and ready to use."""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def write_code(self, tasks: str, feedback: str = "") -> str:
        """Write code based on tasks and optional feedback."""
        feedback_text = f"Previous Reviewer Feedback:\n{feedback}\nPlease address the above issues." if feedback else "This is the first implementation."
        
        print_agent_message("Coder Agent", "Writing code...", Fore.BLUE)
        
        code = self.chain.run(tasks=tasks, feedback=feedback_text)
        print_agent_message("Coder Agent", f"Code implementation:\n{code}", Fore.BLUE)
        return code


class ReviewerAgent:
    """Agent responsible for reviewing and testing code."""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMPERATURE_ANALYTICAL
        )
        
        self.prompt = PromptTemplate(
            input_variables=["code", "tasks"],
            template="""You are a Senior Code Reviewer. Review the following code carefully.

Original Tasks:
{tasks}

Code to Review:
{code}

Provide a review that includes:
1. Does the code meet the requirements? (Yes/No)
2. Code quality issues (if any)
3. Potential bugs or edge cases
4. Suggestions for improvement

If the code is good, say "APPROVED". If it needs changes, list specific issues to fix."""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def review_code(self, code: str, tasks: str) -> tuple[bool, str]:
        """Review code and return (approved, feedback)."""
        print_agent_message("Reviewer Agent", "Reviewing code...", Fore.GREEN)
        
        review = self.chain.run(code=code, tasks=tasks)
        print_agent_message("Reviewer Agent", f"Review:\n{review}", Fore.GREEN)
        
        approved = "APPROVED" in review.upper()
        return approved, review


class SoftwareDevTeam:
    """Orchestrates the software development team."""
    
    def __init__(self):
        self.manager = ManagerAgent()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()
    
    def develop_feature(self, feature_request: str, max_iterations: int = 3):
        """Develop a feature with the team."""
        print_section("Software Development Team Started")
        
        # Step 1: Manager creates tasks
        tasks = self.manager.create_tasks(feature_request)
        
        # Step 2: Iterative development with review cycles
        approved = False
        feedback = ""
        iteration = 0
        
        while not approved and iteration < max_iterations:
            iteration += 1
            print_section(f"Development Iteration {iteration}")
            
            # Coder writes/revises code
            code = self.coder.write_code(tasks, feedback)
            
            # Reviewer reviews code
            approved, feedback = self.reviewer.review_code(code, tasks)
            
            if approved:
                print_section("✓ Feature Development Complete!")
                print(f"Final code:\n{code}")
                break
            else:
                print_section(f"⚠ Iteration {iteration}: Changes requested")
        
        if not approved:
            print_section("⚠ Maximum iterations reached. Manual review needed.")
        
        return code


def main():
    """Run the software development team example."""
    team = SoftwareDevTeam()
    
    # Example feature request
    feature_request = "Create a Python function that calculates the Fibonacci sequence up to n terms with memoization for optimization"
    
    team.develop_feature(feature_request, max_iterations=2)


if __name__ == "__main__":
    main()
