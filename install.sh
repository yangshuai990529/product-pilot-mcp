#!/bin/bash
set -e

# ==============================================================================
# ProductPilot MCP 一键安装脚本
# 功能：自动检测并安装所有缺失的工具和 Python 依赖
# ==============================================================================

echo "============================================="
echo "🚀 ProductPilot MCP 安装程序启动"
echo "============================================="

# ── 步骤 1：检测 SKILL.md 是否已存在（防重复安装）──────────────────────────
if [ -f ".agents/skills/product-mcp/SKILL.md" ]; then
    echo "ℹ️  检测到本地已存在 Product-MCP 技能配置，跳过重复部署。"
    echo "👉 您已可以直接在聊天框输入 '/product-mcp' 唤醒使用。"
    echo "============================================="
    exit 0
fi

# ── 步骤 2：检测 Python 3（必须 >= 3.9）────────────────────────────────────
echo ""
echo "🔍 [1/4] 检测 Python 环境..."
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    echo "✅ 检测到 Python $PY_VER"
    if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 9 ]; }; then
        echo "❌ 错误：需要 Python 3.9 及以上版本，当前为 $PY_VER"
        echo "   请先升级 Python：https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "❌ 错误：未检测到 Python 3，请先安装 Python 3.9+："
    echo "   macOS:  brew install python3"
    echo "   Ubuntu: sudo apt install python3 python3-pip"
    exit 1
fi

# ── 步骤 3：自动创建虚拟环境（若不存在）────────────────────────────────────
echo ""
echo "🔍 [2/4] 检测 Python 虚拟环境..."
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "⚙️  未检测到虚拟环境，正在自动创建 $VENV_DIR/ ..."
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 已存在虚拟环境 $VENV_DIR/"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"
echo "✅ 虚拟环境已激活"

# ── 步骤 4：自动安装所有缺失的 Python 依赖──────────────────────────────────
echo ""
echo "🔍 [3/4] 检测并安装 Python 依赖..."

# 需要的依赖列表（格式: "import名称 pip包名称"）
REQUIRED_PACKAGES=(
    "mcp mcp[cli]"
    "pypdf pypdf"
    "uvicorn uvicorn"
    "fastapi fastapi"
    "multipart python-multipart"
)

MISSING_PACKAGES=()
for entry in "${REQUIRED_PACKAGES[@]}"; do
    import_name=$(echo "$entry" | awk '{print $1}')
    pip_name=$(echo "$entry" | awk '{print $2}')
    if ! python3 -c "import $import_name" &>/dev/null; then
        echo "  ⚠️  缺少依赖: $pip_name（import '$import_name' 失败）"
        MISSING_PACKAGES+=("$pip_name")
    else
        echo "  ✅ $pip_name 已安装"
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo "⚙️  正在自动安装缺失依赖: ${MISSING_PACKAGES[*]}"
    pip install --upgrade pip -q
    pip install "${MISSING_PACKAGES[@]}"
    echo "✅ 所有缺失依赖已安装完成"
else
    echo "✅ 所有依赖均已就绪"
fi

# ── 步骤 5：下载 SKILL.md 技能文件─────────────────────────────────────────
echo ""
echo "🔍 [4/4] 部署 Product-MCP 技能文件..."
mkdir -p .agents/skills/product-mcp
curl -fsSL "https://raw.githubusercontent.com/yangshuai990529/product-pilot-mcp/main/SKILL.md" \
     -o .agents/skills/product-mcp/SKILL.md
mkdir -p my_pdfs

echo ""
echo "============================================="
echo "🎉 安装成功！Product-MCP 技能已完整部署。"
echo ""
echo "👉 使用方式："
echo "   1. 在聊天框中输入 '/product-mcp' 唤醒此专家"
echo "   2. 将 PPT 参考 PDF 拖入项目 'my_pdfs/' 文件夹"
echo ""
echo "👉 手动启动 MCP Server（如需要）："
echo "   source venv/bin/activate && python3 server.py"
echo "============================================="
