# ProductPilot - 高还原排版与 PDF 风格分析中转站 (MCP 与本地 Skill)

这是一个专为 AI 助手（如 Codex、WorkBuddy、Cursor）定制的专家工具配置库，提供以下核心价值：
1. **防止机密 PDF 参考模版泄露**：云端中转自动解密（内置密码 `AI-123`）并提取版式规律，敏感数据不落地。
2. **防范内容页排版错位（核心修复）**：硬性限制大模型使用多余的 `slide-body` 嵌套，强制采用扁平 DOM，且限制单页内容高度不超过 900px，保证 space-between 完美对齐。
3. **自动化配图与自主生图**：AI 会在生成 HTML 时，调用 `generate_image` 产生配套图片并填入相对路径引用。

本仓库支持**两种接入使用模式**，请根据需要选择：

---

## 🚀 方式一：小白用户一键安装本地技能 (Skill 模式 - 强烈推荐)

不需要任何复杂的云端部署，直接对大模型发指令即可一键下载并配置到本地项目中！

### 1. 一键安装
在您打开的 IDE 聊天框中，**直接对 AI 助手说以下这句话**：

> 帮我运行这行命令以安装 /product-mcp 技能：
> `curl -fsSL https://raw.githubusercontent.com/yangshuai990529/product-pilot-mcp/main/install.sh | bash`

AI 助手会自动在本地终端执行脚本。脚本会自动检测，如果本地已经存在此配置则不会重复覆盖，若无则自动在当前项目根目录下生成 `.agents/skills/product-mcp/SKILL.md` 配置文件。

### 2. 使用方法
* 第一步：将您要模仿风格的任意 PPT/PDF 参考模版文件，拖入项目根目录下的 **`my_pdfs/`** 文件夹中。
* 第二步：在聊天框中输入 **`/product-mcp`** 唤醒此技能。例如：
  > `/product-mcp` 帮我读取本地 `my_pdfs/` 下的 PDF 模版，并把我当前的这个 PRD 转换成大纲。

---

## ⚙️ 方式二：高阶云端 MCP 模式 (Model Context Protocol)

适合需要把文件锁在云端服务器中、免本地任何文件拷贝的高级场景：

### 1. 部署到云端
1. 注册并登录免费的云托管平台 [Render](https://render.com/)。
2. 新建 **Web Service**，并关联本 GitHub 仓库。
3. 参数配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
4. 部署成功后，系统会提供一个公网 HTTPS 链接（例如：`https://您的Render网址.onrender.com`）。

### 2. 在 IDE 客户端配置接入
打开 IDE 的 MCP 配置文件（如 `settings.json`），在 `mcpServers` 里配置该公网链接：

```json
{
  "mcpServers": {
    "product-pilot-expert": {
      "url": "https://您的Render网址链接.onrender.com/sse"
    }
  }
}
```
*配置完成后，您可在新项目的 `AGENTS.md` 规则文档中指导本地 AI 在遇到加密 PDF 时自动 Base64 编码并调用云端 MCP 工具进行解密特征提取。*
