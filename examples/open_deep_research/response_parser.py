import re

def parse_agent_response(response):
    """结构化解析API响应"""
    result = {
        "final_answer": "",
        "execution_steps": [],
        "search_links": []
    }
    
    current_step = {}
    link_pattern = re.compile(r'https?://\S+')
    # 新增详细结果匹配模式
    detail_pattern = re.compile(r'### 2\. Task outcome \(extremely detailed version\):(.+?)(?=### 3|\Z)', re.DOTALL)

    for msg in response:
        content = str(msg.get('content', ''))
        metadata = msg.get('metadata', {})
        
        # 解析最终答案
        if "Final answer:" in content:
            result["final_answer"] = _extract_final_answer(content)
        
        # 解析执行步骤（仅处理assistant消息）
        if msg.get('role') == 'assistant' and content.startswith("**Step"):
            current_step = {
                "title": content.strip('* '),
                "details": []
            }
            result["execution_steps"].append(current_step)
        elif current_step and msg.get('role') == 'assistant':
            # 精确提取详细分析内容
            if (detail_match := detail_pattern.search(content)):
                cleaned_content = re.sub(r'\*{2,}|`{3,}', '',
                    detail_match.group(1)).strip()
                current_step["details"].append(cleaned_content)
        
        # 提取执行日志中的链接
        if metadata.get('title') == '📝 Execution Logs':
            result["search_links"].extend(
                link_pattern.findall(content)
            )

    return result

def _extract_final_answer(content):
    """提取并清理最终答案，将字典格式转换为Markdown"""
    # 提取Final answer后的内容
    answer = content.split("Final answer:")[-1].strip()
    # 移除星号等标记
    answer = re.sub(r'\*{2,}', '', answer).strip()
    
    # 检查是否为字典格式
    dict_match = re.search(r'\{.*\}', answer, re.DOTALL)
    if dict_match:
        try:
            # 尝试提取novelty_score和report
            score_match = re.search(r"'novelty_score':\s*(\d+)", answer)
            report_match = re.search(r"'report':\s*'(.*?)'(?=\}$|\}\s*$)", answer, re.DOTALL)
            
            if score_match and report_match:
                # 提取分数
                score = f"# Novelty Score: {score_match.group(1)}/100"
                
                # 提取并清理报告内容
                report = report_match.group(1)
                # 处理转义字符
                report = report.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"')
                
                # 返回格式化的Markdown
                return f"{score}\n\n{report}"
        except Exception:
            pass
    
    # 如果不是字典格式或解析失败，返回原始内容
    return answer

def save_as_markdown(result, filename):
    """生成优化后的Markdown报告"""
    with open(filename, 'w', encoding='utf-8') as f:
        # 最终答案部分
        f.write("## MoonshotAI: Your Startup Novelty Deep Research Report\n")
        f.write(result["final_answer"] + "\n")
        
        # 研究步骤部分 - 添加步骤去重
        if result["execution_steps"]:
            f.write("\n### Execution Steps\n")
            seen_steps = set()
            unique_steps = []
            
            for step in result["execution_steps"]:
                # 使用标题和详情内容作为唯一性判断
                step_content = (step['title'], tuple(step['details']))
                if step_content not in seen_steps:
                    seen_steps.add(step_content)
                    unique_steps.append(step)
            
            # 输出去重后的步骤
            for step in unique_steps:
                f.write(f"\n#### {step['title']}\n")
                f.write('\n'.join(step["details"]) + "\n")
        
        # 搜索结果部分
        if result["search_links"]:
            f.write("\n### Relevant References\n")
            seen = set()
            for raw_link in result["search_links"]:
                # 更强大的链接清理逻辑
                # 1. 移除URL参数
                link = raw_link.split('?')[0]
                # 2. 处理链接后的额外内容（包括括号和换行符）
                link = re.sub(r'\).*$', '', link)
                # 3. 清理各种特殊字符
                link = re.sub(r'[\\n\s.]+$', '', link)
                # 4. 处理链接中的Markdown格式
                link = re.sub(r'\]\(.*$', '', link)
                
                if link and link.startswith('http') and link not in seen:
                    seen.add(link)
                    f.write(f"- {link}\n")
            
            # 移除重复链接输出
            # f.write('\n'.join([f"- {link}" for link in result["search_links"]]))

if __name__ == "__main__":
    import json
    import os
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 使用相对路径构建文件路径
    json_path = os.path.join(current_dir, "last_result.json")
    report_path = os.path.join(current_dir, "analysis_report.md")
    
    # 从本地JSON文件加载数据
    with open(json_path, encoding="utf-8") as f:
        test_data = json.load(f)
    
    parsed_result = parse_agent_response(test_data)
    save_as_markdown(
        parsed_result,
        report_path
    )
    print(f"完整分析报告已保存至：{report_path}")