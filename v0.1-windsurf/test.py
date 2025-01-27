# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-33d8d3c6326a462c89b2d33b9abd4a6b", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "you are a math professor"},
        {"role": "user", "content": "Hello, 你是数学教授，在写一个讲义，希望有证明细节，指出数学关键点。讲义依次涵盖： 历史介绍, 基础知识回顾,数学概念的直观介绍，必要时可以以一个例子辅助, 介绍所需的严格的数学定义, 把核心的数学推理整理成定理的形式, 介绍证明的梗概 , 最后加一些备注， 强调一些关键点和容易理解错误的点。帮我写一个讲义和ppt， 内容主要关于：黎曼积分的介绍。以下是我希望有的内容：介绍一下反常黎曼积分。再介绍下lebesgue积分的想法。"},
    ],
    stream=False
)

print(response.choices[0].message.content)


# test_prompt = "please help me generate a course and its ppt for linear algebra including history, basic background, definitions and examples for linear algebra"