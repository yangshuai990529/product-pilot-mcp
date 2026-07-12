import os
import io
import glob
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
DECRYPT_PASSWORD = "AI-123"

@mcp.tool()
def get_agents_rules() -> str:
    """获取最新优化版的产品演示文稿设计规范、文字层级限制、自动配图规则与海外大师逻辑论证框架。

    本地 AI 助手在生成 PPT（尤其是 HTML 网页幻灯片）时必须严格遵守本规则。
    """
    rules = """
# AI Agent 行为规则 (AGENTS.md - 核心规范)

## 1. 语言与文风规则
* **简体中文默认**：所有生成的文档、PRD、PPT 文案等默认使用**简体中文**。
* **专业术语规范**：专业英文术语首次出现时，必须采用 `中文名称（English Name）` 的格式。
* **拒绝营销词汇**：文案必须使用客观、专业、可测试的产品语言。禁止使用“功能赋能”、“颠覆创新”等营销词汇。

## 2. 逻辑论证架构优化（借鉴海外大厂/咨询公司经典 PPT 框架）
为了使生成的内容极其详细且富有洞察力，必须放弃平铺直叙的文字，转而使用以下海外经典逻辑论证顺序来优化幻灯片大纲：
* **SCQA（情景-冲突-疑问-回答）故事线**：
  - **S (Situation/背景)**：陈述用户熟悉且没有争议的事实或现状（如：画质行业 HDR 趋势和面板普及）。
  - **C (Conflict/冲突)**：指出在背景下出现的关键矛盾或挑战（如：大V评测相机偏色，导致画质口碑下滑）。
  - **Q (Question/疑问)**：针对冲突提出核心解决诉求（如：如何建立高还原度的白平衡校准流程？）。
  - **A (Answer/回答)**：给出我们完整的产品与算法解决方案。
* **金字塔原理（Pyramid Principle）**：
  - **结论先行**：每页 PPT 的 L2 核心结论必须能够独立成章，直击要害。
  - **以上统下 & 归类分组**：下层 L4-L5 核心要点必须是上层 L3 模块的严密分支，每条信息必须有充分的研究细节或数据支持（如：具体人天、具体技术通道、具体色准参数 delta E 范围），生成的内容必须非常详细，禁止一句话概括。

## 3. TCL 官方视觉模板锁（硬性限制）
* **视觉样式绝对禁止变更**：虽然大模型在文案和逻辑上可以借鉴海外 PPT 的深度论证细节，但生成的 HTML 网页幻灯片在 DOM 树和 CSS 样式表上**必须 100% 保持 TCL 官方经典白底红标风格**。
* **锁定品牌特征**：必须使用 TCL 经典品牌红（`#E60012`）、TCL SVG 企业 Logo 与奥运五环水印、红色标题底部分割线（`.title-divider`）、浅灰圆角卡片（`.gray-card`）等。禁止擅自修改任何原本的 CSS 颜色变量与布局边距。

## 4. HTML 网页幻灯片布局限制与自适应规范 (HTML Slides Layout Guidelines)
* **4.1 扁平化 DOM 结构限制 (Don'ts)**：
  - **禁止引入全局包裹器**：在普通内容页（.slide 容器）内部，**严禁**引入 <div class="slide-body">、<div class="wrapper"> 等嵌套层。这会导致 Flexbox 的垂直 space-between 空间分配机制完全失效，产生内容整体下移和上部大片空白的排版故障。
  - **组件平铺原则**：页面的所有核心逻辑大块（如 slide-header, section-banner, grid-x-col, slide-footer）**必须直接作为 .slide 容器的直系子元素 (Direct Children)**。
* **4.2 容器高度与拉伸规范 (Do's)**：
  - **内部高度自适应**：在直系子元素（如卡片组 .grid-4-col）内部放置子卡片时，子卡片的高度建议设置为 height: 100% 或 flex-grow: 1，以保证垂直方向自动拉伸整齐。**严禁在直系子元素（如卡片组）上使用行内样式 style="flex: 0 0 auto;" 或者是 style="flex-grow: 0;"**，这会覆盖原本 CSS 的拉伸属性从而导致排版顶部出现大范围空白。
  - **间距留白限制**：严禁在直系子元素上随意使用大数值的 margin-top、padding-top。所有的垂直分布和留白应完全交由父级容器的 justify-content: space-between 自动计算分发。
  - **900px 垂直高度防溢出条件**：单页中所有直系子元素的高度（包括 margins 和 paddings）累加**不得超过 900px**。这能确保在 16:9 画布（高 1080px）内即使在不同分辨率下，底部的页脚和核心内容也绝不会因高度溢出而被截断。

## 5. 自动化配图规范 (Automatic Image Generation & Embedding)
* **严禁无图或使用文字占位**：在生成 HTML 幻灯片时，所有需要图片、示意原型、架构图或场景插图的区域，**必须放置真实的图片，绝对禁止使用文字描述或空白灰色块占位**。
* **获取图片的合法途径与执行逻辑**：
  - **AI 自主生图（优先推荐）**：您在输出 HTML 之前，必须先根据当前页面的主题（如：量子点背光、电视画质评测等），主动调用内置的 `generate_image` 工具生成高清配图。
  - **路径引用规范**：生成的图片必须统一存储在本地相对路径：`assets/images/` 目录下（如 `assets/images/quantum_dots_structure.png`）。并在 HTML 的 <img> 标签中直接使用此相对路径引用：`<img src="assets/images/quantum_dots_structure.png" alt="量子点结构">`。
  - **公网免版权图源（备用）**：若属于通用风景或科技氛围图，也可以使用合法的公网无版权图库链接（如 Unsplash 链接）。
* **排版防塌陷规范**：图片标签 <img> 的外部必须使用容器（如 .img-container）包裹，且图片样式需声明 width: 100%; height: 100%; object-fit: cover;，防止图片原图比例不一撑毁 PPT 的 Grid 布局。
"""
    return rules

@mcp.tool()
def allocate_and_orchestrate_tasks(user_goal: str) -> str:
    """接收用户的汇报 PPT 总目标，作为 Orchestrator 总调度角色，将任务合理拆分并分配给 4 个协同 Agent。

    参数:
        user_goal: 用户希望达成的 PPT 汇报目标（如：画质项目偏色校准汇报）
    """
    logger.info(f"开始为目标分配 Agent 任务: {user_goal}")
    
    orchestration_plan = f"""
# ProductPilot 多 Agent 协同作战与任务分配计划

针对您的总目标：**“{user_goal}”**，系统已自动拆分为 4 个虚拟 Agent 的协同流水线。AI 助手将依次扮演这 4 个角色来交付高品质、有深度且格式精准的 PPT 幻灯片：

```mermaid
graph TD
    UserGoal["总目标: {user_goal}"] --> R_Agent["1. 行业研究 Agent (数据背景)"]
    R_Agent --> PM_Agent["2. 产品逻辑 Agent (SCQA 金字塔架构)"]
    PM_Agent --> C_Agent["3. 文案细化 Agent (L1-L6 高细节文案)"]
    C_Agent --> UI_Agent["4. 视觉呈现 Agent (AI 配图 + TCL 模板渲染)"]
```

---

## 协同 Agent 职责与 TODO 任务分配：

### 🛠️ 角色 1：行业研究 Agent (Research Agent)
* **核心职责**：通过自动检索本地文档，获取准确的现状背景数据。
* **子 TODO 任务**：
  1. 调用 `search_local_knowledge` 快速检索项目中相关的 PRD、系统需求和技术白皮书。
  2. 提取出画质评测现状、用户反馈的痛点数据（如偏色比例、退货率或大V视频数）。
  3. 为后续幻灯片提供坚实、可测试的原始数据支撑。

### 🛠️ 角色 2：产品逻辑 Agent (PM Agent)
* **核心职责**：提炼幻灯片整体骨架与 SCQA 故事线。
* **子 TODO 任务**：
  1. 借鉴海外大厂/咨询公司经典 PPT 框架，设计 SCQA 论证逻辑。
  2. 编写第 1-2 页的“现状背景（S）”与“体验痛点/冲突（C）”关系。
  3. 设计“解决方案（Q -> A）”的逻辑演进大纲，遵守金字塔原理，结论先行。

### 🛠️ 角色 3：文案细化 Agent (Copywriter Agent)
* **核心职责**：将逻辑骨架扩展为每个页面的 L1-L6 高度详细的文案内容。
* **子 TODO 任务**：
  1. 严禁简单用一句话带过卡片要点。L4 要点控制在 12-25 字，必须有 delta E 参数、具体工时描述、具体技术算法名（如 AWB、三色激光校准）。
  2. L5 辅助描述必须补充完整的技术因果链（如“因为窄带背光光谱与Sensor RGB响应不匹配”）。

### 🛠️ 角色 4：视觉呈现 Agent (UI/UX Agent)
* **核心职责**：视觉卡片图片匹配，并套用 TCL 经典模板进行单文件自包含 HTML 代码的生成。
* **子 TODO 任务**：
  1. 识别卡片和封面所需的配图，主动调用 `generate_image` 生图工具在本地生成高品质图片（存入 `assets/images/`），绝不留白。
  2. 严禁在 HTML 网页中使用 `<div class="slide-body">` 嵌套层，所有页面核心元素必须作为 `.slide` 容器的直系子元素。
  3. 锁死 TCL 品牌红 (`#E60012`)，确保整体排版高度对称、两端对齐。
"""
    return orchestration_plan

@mcp.tool()
def search_local_knowledge(query: str) -> str:
    """自动检索项目本地的所有文档文件（.md, .txt, .json, .html, .prd），快速抓取与关键词相关的详细业务与技术内容。

    参数:
        query: 待检索的核心关键词（例如：AWB, 偏色, 痛点, miniLED）
    """
    logger.info(f"正在本地快速检索知识: {query}")
    
    # 允许检索的项目文件格式
    extensions = ["*.md", "*.txt", "*.json", "*.html", "*.prd", "*.js", "*.css"]
    cwd = os.getcwd()
    
    matches = []
    # 递归遍历除 venv, git 等特殊文件夹以外的本地文件
    for ext in extensions:
        files = glob.glob(os.path.join(cwd, "**", ext), recursive=True)
        for filepath in files:
            # 排除虚拟环境和 git 缓存
            if "venv" in filepath or ".git" in filepath or "node_modules" in filepath:
                continue
                
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                if query.lower() in content.lower():
                    # 匹配成功，提取包含关键词的行及上下文
                    lines = content.split("\n")
                    matched_lines = []
                    for idx, line in enumerate(lines):
                        if query.lower() in line.lower():
                            start = max(0, idx - 1)
                            end = min(len(lines), idx + 2)
                            matched_lines.append(f"  - 行 {idx+1}: " + "\n    ".join(lines[start:end]))
                            # 限制单个文件匹配的最多行数，防止上下文撑爆
                            if len(matched_lines) >= 3:
                                break
                                
                    rel_path = os.path.relpath(filepath, cwd)
                    matches.append(f"📂 **文件**: [{rel_path}](file://{filepath})\n" + "\n".join(matched_lines))
            except Exception as e:
                # 忽略读取失败的文件
                pass
                
    if not matches:
        return f"在本地 Workspace 中未检索到与关键词 '{query}' 相关的文档信息。"
        
    result_summary = f"### 本地知识检索成功 (关键词: '{query}')\n共找到 {len(matches)} 处相关参考：\n\n" + "\n\n".join(matches[:5])
    return result_summary

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
