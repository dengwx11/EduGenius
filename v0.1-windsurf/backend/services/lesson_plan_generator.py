from dotenv import load_dotenv
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agent_manager import AgentManager

load_dotenv()

class LessonPlanGenerator:
    def __init__(self):
        self.agent_manager = AgentManager()

    def generate(self, outline):
        """
        Generate a detailed lesson plan based on the outline
        
        Args:
            outline (str): Teacher's outline for the lesson
            
        Returns:
            dict: Dictionary containing the lesson plan sections
        """
        # Generate content using Autogen agents
        response = self.agent_manager.generate_content(outline)
        return response['lesson_plan']
