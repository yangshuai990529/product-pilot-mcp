#!/bin/bash

# 1. 创建本地项目的技能存放目录
mkdir -p .agents/skills/product-mcp

# 2. 从 GitHub 下载 SKILL.md 技能文件
echo "正在从 GitHub 下载 Product-MCP 技能文件..."
curl -fsSL "https://raw.githubusercontent.com/yangshuai990529/product-pilot-mcp/main/SKILL.md?t=\$(date +%s)" -o .agents/skills/product-mcp/SKILL.md

# 3. 创建本地 PDF 参考文件夹以方便用户放入文件
mkdir -p my_pdfs

echo "============================================="
echo "🎉 安装成功！Product-MCP 技能已部署到本地项目。"
echo "👉 1. 请在聊天框中通过输入 '/product-mcp' 唤醒此专家。"
echo "👉 2. 请把您的 PPT 参考 PDF 模版直接拖入项目本地新创建的 'my_pdfs/' 文件夹下。"
echo "============================================="
