import subprocess
import time
#import pdfkit
import re

def launch_app():
    """启动Gradio应用并获取公共URL"""
    app_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 等待并捕获公共URL
    public_url = None
    for line in iter(app_process.stdout.readline, ''):
        print(line.strip())
        url_match = re.search(r'Running on public URL: (https?://\S+)', line)
        if url_match:
            public_url = url_match.group(1)
            break
            
    if not public_url:
        raise RuntimeError("未能获取Gradio公共URL")
        
    return app_process, public_url

def run_api_test(public_url):
    """执行API测试并生成JSON结果"""
    subprocess.run(
        ["python", "api_test.py", public_url],
        check=True
    )

def generate_markdown():
    """生成Markdown报告"""
    subprocess.run(
        ["python", "response_parser.py"],
        check=True
    )

stop = '''
def convert_to_pdf():
    """将Markdown转换为PDF"""
    markdown_path = r"D:\007.Projects\008.deep_research\smolagents\examples\open_deep_research\analysis_report.md"
    pdf_path = r"D:\007.Projects\008.deep_research\smolagents\examples\open_deep_research\analysis_report.pdf"
    
    # 使用wkhtmltopdf进行转换
    options = {
        'encoding': 'UTF-8',
        'custom-header': [
            ('Content-Encoding', 'UTF-8')
        ]
    }
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    pdfkit.from_string(html_content, pdf_path, options=options)
    return pdf_path
'''

if __name__ == "__main__":
    try:
        # 1. 启动Gradio应用
        app_proc, url = launch_app()
        print(f"\n🚀 Gradio应用已启动: {url}")
        
        # 2. 执行API测试
        print("\n🔧 正在执行API测试...")
        run_api_test(url)
        
        # 3. 生成Markdown报告
        print("\n📝 正在生成分析报告...")
        generate_markdown()
        
        # 4. 转换为PDF
        #print("\n🔄 正在转换为PDF格式...")
        #pdf_path = convert_to_pdf()
        
        #print(f"\n✅ 流程完成！最终报告路径：{pdf_path}")
        
    except Exception as e:
        print(f"\n❌ 流程执行出错: {str(e)}")
    finally:
        # 关闭Gradio进程
        if 'app_proc' in locals():
            app_proc.terminate()