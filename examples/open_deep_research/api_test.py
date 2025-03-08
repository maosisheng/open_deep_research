
from gradio_client import Client
import sys
import os
import time
from dotenv import load_dotenv
import json
import uuid  # 添加uuid模块

# 记录开始时间
start_time = time.time()

# 加载环境变量
load_dotenv()

# 获取 Hugging Face 令牌
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    print("错误：未找到 HF_TOKEN 环境变量。请设置您的 Hugging Face 令牌。")
    sys.exit(1)

# 修改Client初始化，添加认证令牌
client = Client("MaoShen/Moonshot_DeepResearch", hf_token=hf_token)

# First log the user message
log_result = client.predict(
    text_input=""" 
there is an Startup idea -"Using the reasoning llm to help the startup evaluate  their ideas' quality and novelty, finally help them improve their ideas"
Do you think this startup idea is of great novelty? research this idea from three perspectives and generate a novelty score:
1.Problem Uniqueness: Does this idea address an unmet or unrecognized need?
2.Existing Solution: Including competitors (the most important), patent and intellectual property research, and academic research,
3. Differentiation: Conduct research from technical innovation, business model innovation, market segment, and user experience.
Give your final answer as detailed as professinal as possible in the following format:
A Novelty Score on a scale of 100.
A report over 5000 words including sections of Overview, Problem Uniqueness, Existing Solution, Differentiation, Conclusion, and Sources & References (show all the sources in hyperlink)
You should have intext Citation in the final answer content with proper hyperlink. Note the hyperlink is a must, you should make each intext ciation hyperlink. 
""",
    api_name="/log_user_message"
)

# 生成唯一会话ID和消息ID
session_id = str(uuid.uuid4())
message_id = str(uuid.uuid4())

# Then interact with agent using the logged message
result = client.predict(
    messages=[{
        "role": "user",
        "content": log_result,
        "metadata": {
            "id": message_id,
            "parent_id": session_id
        }
    }],
    api_name="/interact_with_agent_1"
)

# 使用相对路径保存结果
current_dir = os.path.dirname(os.path.abspath(__file__))
result_file = os.path.join(current_dir, "last_result.json")

try:
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 计算并输出总执行时间
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"API响应结果已保存至：{result_file}")
    print(f"脚本总执行时间：{execution_time:.2f} 秒")
except Exception as e:
    print(f"保存结果时出错: {str(e)}")

