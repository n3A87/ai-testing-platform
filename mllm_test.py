import base64
from zhipuai import ZhipuAI

img_path = "static/data/pic/1.jpg"

with open(img_path,"rb") as img_file:
    # 在图像领域，传递图片和保存图片一般是base64格式
    img_base = base64.b64encode(img_file.read()).decode("utf-8")

client = ZhipuAI(api_key="kkkkkkkkkkkkkkkkkkkk")
response = client.chat.completions.create(
    model="glm-4v-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_base
                    }
                },
                {
                    "type": "text",
                    "text": "请描述这个图片"
                }
            ]
        }
    ]
)
print(response.choices[0].message)