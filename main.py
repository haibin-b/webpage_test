from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai
from datetime import datetime

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_content(prompt):
    """使用OpenAI生成内容"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的网页内容生成助手。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成内容时出错: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_info = data.get('user_info', {})
    
    # 生成个人介绍
    intro_prompt = f"请根据以下信息生成一段个人介绍：{user_info}"
    introduction = generate_content(intro_prompt)
    
    # 生成教育背景
    education_prompt = f"请根据以下信息生成教育背景描述：{user_info}"
    education = generate_content(education_prompt)
    
    # 生成技能描述
    skills_prompt = f"请根据以下信息生成技能描述：{user_info}"
    skills = generate_content(skills_prompt)
    
    # 生成项目经历
    projects_prompt = f"请根据以下信息生成项目经历描述：{user_info}"
    projects = generate_content(projects_prompt)
    
    return jsonify({
        'introduction': introduction,
        'education': education,
        'skills': skills,
        'projects': projects
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 