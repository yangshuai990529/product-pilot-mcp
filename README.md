# ProductPilot - 高级内容排版与 PDF 风格分析中转站 MCP 服务

这是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 协议构建的独立微服务，旨在解决以下三大痛点：
1. **防范机密 PDF 模版泄露**：敏感的 PPT/PDF 文件在本地是加密的（打开密码 `ys911..ob`）。本地的 AI 助手通过将加密 PDF 作为 Base64 发送给此云端服务，由云端解密并分析风格返回，实现“敏感文件不落地”。
2. **规避网页幻灯片排版错位（关键修复）**：内置了针对大模型容易多写 `.slide-body` 导致 Flexbox 空间分配机制失效、内容下移溢出等问题的优化排版限制规范。
3. **内置自动化配图与生图条件**：指导大模型在渲染网页幻灯片时主动调用本地/云端生图接口，输出完整的本地图片路径，拒用空白占位符。

---

## 🛠️ 其他 AI 助手 / 客户端配置步骤 (一键集成)

别人要使用您的这个 MCP 工具，只需要在他们的 IDE（如 Codex、WorkBuddy 或 Cursor）的全局 MCP 配置文件中加入此服务的链接。

### 1. 本地 Stdio 运行模式配置 (直接从 GitHub 远程运行)
如果不需要部署云端，客户端直接通过命令行自动从您的 GitHub 仓库拉取并启动：

#### A. Node.js (npx) 启动配置：
若用 Node 运行，在 `settings.json` 的 `mcpServers` 对象中添加：
```json
"mcpServers": {
  "product-pilot-expert": {
    "command": "npx",
    "args": [
      "-y",
      "git+https://github.com/yangshuai990529/product-pilot-mcp.git"
    ]
  }
}
```

#### B. Python (uvx) 启动配置（极速拉取运行）：
```json
"mcpServers": {
  "product-pilot-expert": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/yangshuai990529/product-pilot-mcp.git",
      "mcp"
    ]
  }
}
```

---

### 2. 远程 SSE 运行模式配置 (一键部署至 Render/Railway)
如果您不希望把代码包（包含 PDF 加密算法）下载到别人的本地缓存中，推荐部署在 Render 平台上：
1. 在 [Render.com](https://render.com/) 新建一个 **Web Service**，并绑定您的 GitHub 仓库。
2. 填写配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
3. 部署成功后，得到一个公网链接，如 `https://product-pilot-mcp-xxxx.onrender.com`。
4. 别人在其本地 IDE 的 `settings.json` 中配置您的公网 SSE 入口即可：
   ```json
   "mcpServers": {
     "product-pilot-expert": {
       "url": "https://您的Render网址链接.onrender.com/sse"
     }
   }
   ```

---

## 📄 项目级 AI 助手规则配置 (AGENTS.md)

在新项目的根目录下，将以下规则追加到 `AGENTS.md` 的末尾，使 AI 助手懂得在遇到本地加密 PDF 时自动运行 Python 脚本生成 Base64 流，并调用此 MCP 进行前置分析：

```markdown
## 关于加密 PDF 参考模版的风格分析规则

* 当您（AI 助手）需要对本地 `examples/ppt/` 下的加密 PDF 进行风格前置分析时，必须使用本地运行脚本，在后台执行一段 Python 将该加密文件转化为 Base64 编码字符串。
* 然后，调用 MCP 提供的 `extract_and_analyze_pdf` 工具，将 Base64 发送到云端。
* 云端会自动使用密码 `ys911..ob` 进行解密，并为您返回风格特征分析报告。
```
