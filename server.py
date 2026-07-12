import os
import io
import base64
import logging
import uvicorn
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader

# 配置基本的日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ppt-expert-server")

# 初始化 FastMCP
mcp = FastMCP("ppt-expert-server")

# 统一的加密 PDF 打开密码
DECRYPT_PASSWORD = "ys911..ob"

@mcp.tool()
def get_agents_rules() -> str:
    """获取产品设计、文风和文字层级 (L1-L6) 的系统级行为准则。

    本地 AI 助手在生成 PPT 文案时必须严格遵循本规则。
    """
    rules = """
# AI Agent 行为规则 (AGENTS.md - 核心规范)

## 1. 语言与文风规则
* **简体中文默认**：除非用户明确要求英文，否则所有生成的文档、PRD、PPT 文案、页面说明、错误提示和代码注释均默认使用**简体中文**。
* **专业术语规范**：专业英文术语首次出现时，必须采用 `中文名称（English Name）` 的格式（例如：系统需求（System Requirement，SR））。
* **拒绝营销词汇**：文案必须使用客观、专业、可测试的产品语言。禁止使用空洞无物的营销词汇，如“赋能”、“引领未来”、“颠覆创新”等。
* **简洁高效**：结论明确、逻辑完整、避免大段文字，能用图表/对比矩阵表达的绝不用纯文本。

## 2. 文字层级规范 (L1 - L6)
* **L1：页面主标题**：控制在 6–18 个中文字符，表达核心主题，不使用完整长句。
* **L2：页面副标题/核心结论**：控制在 20–40 个中文字符，使用一句完整的话表达本页的核心判断。
* **L3：模块标题**：用于区分不同内容模块（例如：当前现状、问题原因、影响范围、产品方案、用户价值）。
* **L4：功能点/关键要点**：控制在 12–25 个中文字符，每条表达一个独立的、可开发或可测试的信息。
* **L5：辅助说明**：补充条件、限制、备注等，字号明显小于正文，仅在必要时使用。
* **L6：页脚/保密信息**：包括数据来源、文档版本、更新时间、保密标识等。

## 3. 视觉与排版强制要求
* 每页 PPT **必须至少包含一种有效的视觉内容**（真实截图、示意原型、流程图、架构图、对比图、数据图表或场景图片）。
* **严禁生成纯文字页面**。若缺少实际素材，必须生成清晰标注的可替换示意内容。
"""
    return rules

@mcp.tool()
def extract_and_analyze_pdf(file_name: str, base64_content: str) -> str:
    """接收本地发送的 PDF Base64 编码数据，在云端自动解密（针对加密PDF）并解析，提取其结构与风格特征。

    参数:
        file_name: 上传的文件名称（用于日志和识别）
        base64_content: PDF 文件的 Base64 编码字符串
    """
    logger.info(f"开始解析上传的 PDF 文件: {file_name}")
    try:
        # 1. 解码 Base64
        pdf_data = base64.b64decode(base64_content)
        pdf_file = io.BytesIO(pdf_data)
        
        # 2. 读取 PDF
        reader = PdfReader(pdf_file)
        
        # 3. 判断并尝试解密
        is_encrypted = reader.is_encrypted
        if is_encrypted:
            logger.info(f"检测到加密 PDF: {file_name}，正在尝试自动解密...")
            # 尝试使用硬编码密码解密
            success = reader.decrypt(DECRYPT_PASSWORD)
            if not success:
                # 尝试用空密码解密（有些PDF只是限制编辑而没有打开密码）
                success = reader.decrypt("")
            
            if not success:
                return f"解析失败：文件 '{file_name}' 已加密，且无法使用系统内置密码自动解密。"
            logger.info(f"加密文件 '{file_name}' 已成功解密。")

        # 4. 提取信息（限制读取前 5 页以防止超出上下文限制，并只提取大纲和核心文本）
        total_pages = len(reader.pages)
        pages_to_read = min(total_pages, 5)
        
        extracted_content = []
        extracted_content.append(f"### 模版基本信息")
        extracted_content.append(f"- **文件名**: {file_name}")
        extracted_content.append(f"- **总页数**: {total_pages} 页")
        extracted_content.append(f"- **加密状态**: {'是（已自动解密）' if is_encrypted else '否'}")
        extracted_content.append(f"- **读取样本数**: 前 {pages_to_read} 页\n")
        
        extracted_content.append("### 各页内容大纲与版式特征")
        for index in range(pages_to_read):
            page = reader.pages[index]
            text = page.extract_text() or ""
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            
            extracted_content.append(f"#### 第 {index + 1} 页特征")
            if lines:
                # 猜测标题（第一行通常是标题）
                title = lines[0]
                extracted_content.append(f"- **可能标题**: {title}")
                extracted_content.append(f"- **关键内容抽样**:")
                # 抽样提取几行文本作为结构参考
                for line in lines[1:8]:
                    extracted_content.append(f"  - {line}")
                if len(lines) > 8:
                    extracted_content.append(f"  - （余下 {len(lines) - 8} 行内容省略...）")
            else:
                extracted_content.append("- （未提取到文本内容，可能该页为纯图片或扫描版页面）")
            extracted_content.append("")
            
        analysis_result = "\n".join(extracted_content)
        logger.info(f"PDF 文件 '{file_name}' 解析与分析完成。")
        return analysis_result

    except Exception as e:
        logger.error(f"处理 PDF 发生异常: {str(e)}")
        return f"处理 PDF 发生错误: {str(e)}"

if __name__ == "__main__":
    # Render 等云平台会自动注入 PORT 环境变量，如果没有则默认为 8000
    port = int(os.environ.get("PORT", 8000))
    # 启动 ASGI Web 容器以提供 SSE (Server-Sent Events) 服务
    logger.info(f"启动 MCP SSE 服务，监听端口: {port}...")
    uvicorn.run(mcp.asgi(), host="0.0.0.0", port=port)
