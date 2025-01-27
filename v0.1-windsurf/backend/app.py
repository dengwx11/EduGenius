from flask import Flask, request, jsonify
from flask_cors import CORS
from services.ppt_generator import PPTGenerator
from services.lesson_plan_generator import LessonPlanGenerator

app = Flask(__name__)
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        outline = data.get('outline')
        
        if not outline:
            return jsonify({'error': 'No outline provided'}), 400

        # Generate PPT and lesson plan
        ppt_generator = PPTGenerator()
        lesson_plan_generator = LessonPlanGenerator()

        ppt_content = ppt_generator.generate(outline)
        lesson_plan = lesson_plan_generator.generate(outline)

        return jsonify({
            'status': 'success',
            'ppt_content': ppt_content,
            'lesson_plan': lesson_plan
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
