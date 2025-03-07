
from gradio_client import Client

# 在文件顶部添加
import sys

# 修改Client初始化
client = Client("https://248d6ac549256e7993.gradio.live/")

# First log the user message
log_result = client.predict(
    text_input=""" 
there is an Startup idea -"Using the reasoning llm to help the startup evaluate  their ideas' quality and noveltyn, finally help them imprve their ideas"
Do you think this startup idea is of great novelty? research this idea from three perspectives and generate a novelty score:
1.Problem Uniqueness: Does this idea address an unmet or unrecognized need?
2.Existing Solution: Including competitors (the most important), patent and intellectual property research, and academic research,
3. Differentiation: Conduct research from technical innovation, business model innovation, market segment, and user experience.
Give your final answer as detailed as professinal as possible in the following format:
A Novelty Score on a scale of 100.
A report over 5000 words including sections of Overview, Problem Uniqueness, Existing Solution, Differentiation, Conclusion, and Sources & References (show all youe sources);
You should have intext Citation in the final answer with number and hyperlink, the hyperlink is a must 
""",
    api_name="/log_user_message"
)

# Then interact with agent using the logged message
result = client.predict(
    messages=[{
        "role": "user",
        "content": log_result,
        "metadata": {
            "id": "1",
            "parent_id": "0"
        }
    }],
    api_name="/interact_with_agent_1"
)

# 在获取result之后添加以下代码
import json

result_file = r"D:\007.Projects\008.deep_research\smolagents\examples\open_deep_research\last_result.json"
with open(result_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"API响应结果已保存至：{result_file}")

