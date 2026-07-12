#!/bin/bash

# 检查本地是否已经存在该技能文件
if [ -f ".agents/skills/product-mcp/SKILL.md" ]; then
    echo "============================================="
    echo "ℹ️ 检测到本地已存在 Product-MCP 技能配置，跳过重复部署。"
    echo "👉 您已可以直接在聊天框输入 '/product-mcp' 唤醒使用。"
    echo "============================================="
    exit 0
fi

# 1. 创建本地项目的技能存放目录
mkdir -p .agents/skills/product-mcp

# 2. 从 GitHub 下载 SKILL.md 技能文件
echo "正在从 GitHub 下载 Product-MCP 技能文件..."
curl -fsSL "https://raw.githubusercontent.com/yangshuai990529/product-pilot-mcp/main/SKILL.md?v=2026" -o .agents/skills/product-mcp/SKILL.md

# 3. 创建本地 PDF 参考文件夹以方便用户放入文件
mkdir -p my_pdfs

echo "============================================="
echo "🎉 安装成功！Product-MCP 技能已部署到本地项目。"
echo "👉 1. 请在聊天框中通过输入 '/product-mcp' 唤醒此专家。"
echo "👉 2. 请把您的 PPT 参考 PDF 模版直接拖入项目本地新创建的 'my_pdfs/' 文件夹下。"
echo "============================================="
