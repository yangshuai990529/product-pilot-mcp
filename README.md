# ProductPilot - PDF 风格解析中转站 MCP 服务

这是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 协议构建的云端风格分析服务，旨在解决以下问题：
1. **防止机密 PDF 参考模版文件泄露**：敏感 PDF 文件经过加密后分发（别人打不开）。AI 助手通过将加密 PDF 作为 Base64 传入该 MCP 服务，在云端自动使用密码解密并提炼风格大纲返回，实现“敏感数据不落地”。
2. **多项目免部署**：用户无需在每个代码仓库中拷贝配置文件或 PDF 文件，只需配置该 MCP 的云端 API 地址即可全局使用。
3. **共享排版与文字规范**：自动为 AI 助手注入 L1-L6 文字层级规范与设计规则。

---

## 🚀 部署指南 (云端 Render/Railway 部署)

您可以将此目录下的代码推送到 GitHub，然后将其部署到 Render 或 Railway 等云平台（提供免费额度）：

### 方式一：部署到 Render (推荐)
1. 将此 `product-pilot-mcp/` 文件夹的代码作为一个单独的仓库推送到您的 GitHub（可以设为 **Private** 私有仓库以确保安全）。
2. 登录 [Render 官网](https://render.com/)，点击 **New** -> **Web Service**。
3. 关联您刚才创建的 GitHub 仓库。
4. 填写配置：
   - **Name**: `product-pilot-mcp`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
5. 点击 **Deploy Web Service**。部署成功后，您会获得一个公网 HTTPS 链接，例如：
   `https://product-pilot-mcp-xxxx.onrender.com`

---

## 🛠️ 配置使用指南 (分发给别人使用)

当您把服务部署好后，别人只需要在他们本地的 IDE 中进行一次配置即可使用。

### 1. Codex / WorkBuddy / VS Code 配置
打开 IDE 的 MCP 配置文件（例如在 Mac 上是 `~/.gemini/config/mcp/settings.json` 或 `~/.config/Cursor/mcp/settings.json`），添加以下配置：

```json
{
  "mcpServers": {
    "product-pilot-expert": {
      "url": "https://您的Render网址链接.onrender.com/sse"
    }
  }
}
```

### 2. 项目级 AI 指令配置
在项目根目录下放一个 `AGENTS.md`，或者直接将以下内容追加到项目已有的 `AGENTS.md` 中。这是为了教会本地的 AI 助手如何调用该云端 MCP：

```markdown
## 关于风格分析 PDF 文件的处理：
1. 项目中的参考 PPT/PDF 模版通常为加密状态，您（AI 助手）及用户在本地均无法直接打开。
2. 当需要进行风格前置分析（读取 `examples/ppt/` 中的 PDF）时，您**必须**调用 `product-pilot-expert` 提供的 `extract_and_analyze_pdf` 工具。
3. **调用方式**：使用本地运行脚本工具，在后台运行 Python 将 PDF 文件读取为 Base64 编码，并将其作为参数传入 `extract_and_analyze_pdf` 工具中，从而获取解密后的风格分析报告。
```

---

## 🔒 附录：如何对本地 PDF 文件进行批量加密？

如果您有新的 PPT/PDF 参考模版想要加入分发，并且不希望别人直接双击打开查看，可以在本地运行以下 Python 脚本对其进行加密（需要安装 `pypdf`：`pip install pypdf`）：

```python
import os
from pypdf import PdfReader, PdfWriter

# 设定加密密码
PASSWORD = "ys911..ob"
# 待加密 PDF 目录
TARGET_DIR = "./my_new_pdfs" 

for filename in os.listdir(TARGET_DIR):
    if filename.endswith(".pdf"):
        filepath = os.path.join(TARGET_DIR, filename)
        reader = PdfReader(filepath)
        writer = PdfWriter()
        
        # 复制所有页面
        for page in reader.pages:
            writer.add_page(page)
            
        # 强加密设置打开密码
        writer.encrypt(PASSWORD)
        
        # 写回覆盖
        with open(filepath, "wb") as f:
            writer.write(f)
            
        print(f"成功加密: {filename}，已限制打开权限。")
```
加密后的 PDF 文件即可安全地打包发送给别人，或者放在项目根目录下供 AI 助手读取上传。
