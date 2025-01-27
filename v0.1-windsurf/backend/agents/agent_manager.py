from typing import Dict, Any, List, Optional
import json
import time
import traceback
from openai import OpenAI
from .config import TEACHER_AGENT_CONFIG, PPT_DESIGNER_CONFIG, LESSON_PLANNER_CONFIG

class CustomAgent:
    def __init__(self, name: str, system_message: str, llm_config: Dict):
        self.name = name
        self.system_message = system_message
        self.llm_config = llm_config
        self.config = llm_config["config_list"][0]
        self.client = OpenAI(
            api_key=self.config["api_key"],
            base_url=self.config["base_url"]
        )
        
    def send(self, message: str):
        print(f"[DEBUG] Entering send() with message: {message[:10]}")
        try:
            print(f"[DEBUG] Attempting API call to {self.config['model']}")
            
            # 记录API调用前的时间戳
            start_time = time.time()
            
            # response = self.client.chat.completions.create(
            #     model=self.config["model"],
            #     messages=[
            #         {"role": "system", "content": self.system_message},
            #         {"role": "user", "content": message}
            #     ],
            #     temperature=self.llm_config.get("temperature", 0.6),
            #     stream=False
            # )
            
            # # 记录响应时间
            # print(f"[PERF] API response time: {time.time() - start_time:.2f}s")
            
            # # 深度调试响应结构
            # # print(f"[DEBUG] Raw response: {vars(response)}")
            # print(f"[DEBUG] Choices count: {len(response.choices)}")
            
            # if not response.choices:
            #     print("[ERROR] Empty choices array")
            #     return None
                
            # first_choice = response.choices[0]
            # #print(f"[DEBUG] First choice: {vars(first_choice)}")
            
            # if not hasattr(first_choice.message, 'content'):
            #     print("[ERROR] Missing content in message")
            #     return None
                
            # response_text = first_choice.message.content
            # print(f"[SUCCESS] Response content: {response_text[:50]}...")  # 截取前50字符
            
            # 记录API调用后的时间戳
            end_time = time.time()
            print(f"[PERF] API call time: {end_time - start_time:.2f}s")

            response_text = "hello world"
            print(f"[SUCCESS] Response content: {response_text[:50]}...")
            
            return response_text
            
        except Exception as e:
            print(f"[CRITICAL] Exception in send(): {str(e)}")
            print(traceback.format_exc())
            return None
        finally:
            print("[DEBUG] Exiting send() function")

class AgentManager:
    def __init__(self):
        # Initialize custom agents
        self.teacher = CustomAgent(
            name=TEACHER_AGENT_CONFIG["name"],
            system_message=TEACHER_AGENT_CONFIG["system_message"],
            llm_config=TEACHER_AGENT_CONFIG["llm_config"]
        )
        self.ppt_designer = CustomAgent(
            name=PPT_DESIGNER_CONFIG["name"],
            system_message=PPT_DESIGNER_CONFIG["system_message"],
            llm_config=PPT_DESIGNER_CONFIG["llm_config"]
        )

    def _get_section_content(self, section: str, outline: str) -> str:
        """Get detailed content for a specific section"""
        prompt = f"""For the following outline about Riemann Integration:
        {outline}
        
        Create detailed mathematical content for the section: {section}
        
        Include:
        1. Rigorous mathematical definitions and theorems
        2. Complete proof sketches and derivations
        3. Step-by-step examples with solutions
        4. Historical context and applications
        5. Common misconceptions and their corrections
        
        Make the content as detailed as possible, with proper mathematical notation."""
        
        return self.teacher.send(prompt)

    def generate_content(self, outline: str) -> Dict[str, Any]:
        """
        Generate both PPT and lesson plan content using the teacher agent
        
        Args:
            outline (str): The lesson outline provided by the teacher
            
        Returns:
            Dict containing both PPT and lesson plan content
        """
        max_attempts = 3  # Set a maximum number of attempts
        attempts = 0
        previous_response = None
        while attempts < max_attempts:
            print(f"Attempt number: {attempts + 1}")  # Log the attempt number
            try:
                print('we are in the try')# Generate detailed content for each section
                sections = [
                    "Historical Development of Riemann Integration",
                    "Limits and Convergence in Riemann Integration",
                    "Formal Definition and Properties",
                    "Computational Techniques and Examples",
                    "Advanced Topics and Applications"
                ]
                
                detailed_content = {}
                for section in sections:
                    content = self._get_section_content(section, outline)
                    detailed_content[section] = content
                
                # Have the PPT designer organize it into slides
                designer_prompt = f"""Create a detailed PowerPoint presentation based on this mathematical content:

                {json.dumps(detailed_content, indent=2)}
                
                Requirements:
                1. Each section should span multiple slides
                2. Include all mathematical definitions and theorems
                3. Show complete proof sketches
                4. Include step-by-step derivations
                5. Add visualization descriptions
                6. Include practice problems with solutions
                
                Respond in JSON format with the following structure:
                {{
                    "ppt_content": {{
                        "slides": [
                            {{"title": "string", "content": "string"}}
                        ],
                        "file_path": "string"
                    }},
                    "lesson_plan": {{
                        "objectives": ["string"],
                        "materials": ["string"],
                        "introduction": "string",
                        "main_content": "string",
                        "practice": "string",
                        "summary": "string",
                        "assessment": "string"
                    }}
                }}"""

                response = self.ppt_designer.send(designer_prompt)
                print('[DEBUG] Exited send() function')
                
                # Log the raw response
                print(f"Response received: {response}")  
                # Validate response structure
                if isinstance(response, dict) and "ppt_content" in response and "lesson_plan" in response:
                    return response
                else:
                    print(f"Unexpected response structure: {response}")
                    attempts += 1
                    previous_response = response
                    print(f"Incrementing attempts: {attempts}")  # Log attempts increment
                    if previous_response == response:
                        print(f"Response has not changed after {attempts} attempts. Breaking the loop.")
                        break  # Break the loop if the response hasn't changed
                    continue  # Retry on unexpected structure
                
            except Exception as e:
                print(f"Error generating content: {str(e)}")
                attempts += 1
                print(f"Incrementing attempts due to error: {attempts}")  # Log attempts increment
                if attempts >= max_attempts:
                    print(f"Max attempts reached. Returning fallback response.")
                    return self._get_fallback_response()  # Return fallback after max attempts reached
        
        print(f"Returning fallback response after {max_attempts} attempts.")
        return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict[str, Any]:
        """Return a fallback response when content generation fails"""
        return {
            "ppt_content": {
                "slides": [
                    {"title": "Error", "content": "Failed to generate content"}
                ],
                "file_path": None
            },
            "lesson_plan": {
                "objectives": ["Error: Failed to generate content"],
                "materials": [],
                "introduction": "",
                "main_content": "",
                "practice": "",
                "summary": "",
                "assessment": ""
            }
        }
