# ProductPilot - 本地极简 Skill 演示文稿专家

这是一个专为 AI 助手（如 Codex、WorkBuddy、Cursor）定制的本地技能包（Skill），旨在通过最简单的一键安装，让 AI 助手能够直接模仿您本地项目文件夹里的 PPT 参考模版，并生成符合规范的演示文稿。

---

## 🚀 小白一键安装指南

在新项目打开的 IDE（Codex / WorkBuddy / Cursor）聊天框中，**直接对 AI 助手说以下这句话**：

> 帮我运行这行命令以安装 /product-mcp 技能：
> `curl -fsSL https://raw.githubusercontent.com/yangshuai990529/product-pilot-mcp/main/install.sh | bash`

AI 助手会自动在您本地项目的终端运行此脚本，并在您的项目根目录下创建所需的配置和文件夹。

---

## 🛠️ 使用步骤

安装完成后，您只需按照以下两步即可直接使用：

### 第一步：拖入您的参考模版
将您想要 AI 模仿其风格的任意 PPT/PDF 参考模版文件，拖入到项目根目录下自动创建好的 **`my_pdfs/`** 文件夹中。

### 第二步：唤醒并使用
在聊天框中直接输入 **`/product-mcp`**，并输入您的要求。例如：

> `/product-mcp` 帮我读取本地 `my_pdfs/` 下的 PDF 模版，并把我当前的这个 PRD 转换成大纲。

AI 助手收到指令后，会自动触发此技能，读取本地 `my_pdfs/` 目录下的 PDF 内容进行前置风格分析，并生成格式完全对齐的幻灯片大纲！
