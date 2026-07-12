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
mcp = FastMCP("product-pilot-expert")

# 统一的加密 PDF 打开密码
DECRYPT_PASSWORD = "ys911..ob"

@mcp.tool()
def get_agents_rules() -> str:
    """获取最新优化版的产品演示文稿设计规范、文字层级限制与自动配图规则。

    本地 AI 助手在生成 PPT（尤其是 HTML 网页幻灯片）时必须严格遵守本规则。
    """
    rules = """
# AI Agent 行为规则 (AGENTS.md - 核心规范)

## 1. 语言与文风规则
* **简体中文默认**：所有生成的文档、PRD、PPT 文案等默认使用**简体中文**。
* **专业术语规范**：专业英文术语首次出现时，必须采用 `中文名称（English Name）` 的格式。
* **拒绝营销词汇**：文案必须使用客观、专业、可测试的产品语言。禁止使用“功能赋能”、“颠覆创新”等营销词汇。

## 2. 文字层级规范 (L1 - L6)
* **L1：页面主标题**：控制在 6–18 个中文字符，表达核心主题。
* **L2：页面副标题/核心结论**：控制在 20–40 个中文字符，使用一句完整的话表达本页的核心判断。
* **L3：模块标题**：用于区分不同内容模块。
* **L4：功能点/关键要点**：控制在 12–25 个中文字符，每条表达一个独立的、可开发或可测试的信息。
* **L5：辅助说明**：补充条件、限制、备注等，字号明显小于正文。
* **L6：页脚/保密信息**：包括数据来源、更新时间、保密标识等。

## 3. HTML 网页幻灯片布局限制与自适应规范 (HTML Slides Layout Guidelines)
为了确保幻灯片内容页的 Flex 垂直分布对齐（justify-content: space-between）与自适应缩放能够正常工作，大模型在生成 HTML 代码时必须严格遵守以下布局条件：

* **3.1 扁平化 DOM 结构限制 (Don'ts)**：
  - **禁止引入全局包裹器**：在普通内容页（.slide 容器）内部，**严禁**引入 <div class="slide-body">、<div class="wrapper"> 等把除 Header/Footer 外的多个内容大块打包在一起的嵌套层。这会导致 Flexbox 的垂直 space-between 空间分配机制完全失效。
  - **组件平铺原则**：页面的所有核心逻辑大块（如 slide-header, section-banner, grid-x-col, slide-footer）**必须直接作为 .slide 容器的直系子元素 (Direct Children)**。

* **3.2 容器高度与拉伸规范 (Do's)**：
  - **内部高度自适应**：在直系子元素（如卡片组 .grid-4-col）内部放置子卡片时，子卡片的高度建议设置为 height: 100% 或 flex-grow: 1，以保证垂直方向自动拉伸整齐。
  - **间距留白限制**：严禁在直系子元素上随意使用大数值的 margin-top、padding-top 或绝对定位把内容往下推。所有的垂直分布和留白应完全交由父级容器的 justify-content: space-between 自动计算分发。
  - **900px 垂直高度防溢出条件**：单页中所有直系子元素的高度（包括 margins 和 paddings）累加**不得超过 900px**。这能确保在 16:9 画布（高 1080px）内即使在不同分辨率下，底部的页脚和核心内容也绝不会因高度溢出而被截断。

## 4. 自动化配图规范 (Automatic Image Generation & Embedding)
* **严禁无图或使用文字占位**：在生成 HTML 幻灯片时，所有需要图片、示意原型、架构图或场景插图的区域，**必须放置真实的图片，绝对禁止使用文字描述或空白灰色块占位**。
* **获取图片的合法途径与执行逻辑**：
  - **AI 自主生图（优先推荐）**：您在输出 HTML 之前，必须先根据当前页面的主题（如：量子点背光、电视画质评测等），主动调用内置的 `generate_image` 工具生成高清配图。
  - **路径引用规范**：生成的图片必须统一存储在本地相对路径：`assets/images/` 目录下（如 `assets/images/quantum_dots_structure.png`）。并在 HTML 的 <img> 标签中直接使用此相对路径引用：`<img src="assets/images/quantum_dots_structure.png" alt="量子点结构">`。
  - **公网免版权图源（备用）**：若属于通用风景或科技氛围图，也可以使用合法的公网无版权图库链接（如 Unsplash 链接）。
* **排版防塌陷规范**：图片标签 <img> 的外部必须使用容器（如 .img-container）包裹，且图片样式需声明 width: 100%; height: 100%; object-fit: cover;，防止图片原图比例不一撑毁 PPT 的 Grid 布局。
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
            success = reader.decrypt(DECRYPT_PASSWORD)
            if not success:
                success = reader.decrypt("")
            
            if not success:
                return f"解析失败：文件 '{file_name}' 已加密，且无法使用系统内置密码自动解密。"
            logger.info(f"加密文件 '{file_name}' 已成功解密。")

        # 4. 提取信息（限制读取前 5 页）
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
                title = lines[0]
                extracted_content.append(f"- **可能标题**: {title}")
                extracted_content.append(f"- **关键内容抽样**:")
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
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"启动 MCP SSE 服务，监听端口: {port}...")
    uvicorn.run(mcp.asgi(), host="0.0.0.0", port=port)
