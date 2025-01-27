from services.ppt_generator import PPTGenerator
from services.lesson_plan_generator import LessonPlanGenerator
import json

def test_content_generation():
    # Test outline
    outline = """
    我们这次来介绍黎曼积分。包含：
    1. 历史
    2. 黎曼积分中用的极限
    3. 黎曼积分的定义
    4. 黎曼积分的计算技巧和实例
    """

    # Initialize generators
    ppt_gen = PPTGenerator()
    lesson_gen = LessonPlanGenerator()

    try:
        # Generate PPT content
        print("Generating PPT content...")
        ppt_content = ppt_gen.generate(outline)
        print("\nPPT Content:")
        print(json.dumps(ppt_content, ensure_ascii=False, indent=2))

        # Generate lesson plan
        print("\nGenerating lesson plan...")
        lesson_plan = lesson_gen.generate(outline)
        print("\nLesson Plan:")
        print(json.dumps(lesson_plan, ensure_ascii=False, indent=2))

        return True

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_content_generation()
