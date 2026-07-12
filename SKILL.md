---
name: product-mcp
description: 演示文稿生成与风格校准专家 (Generate slides based on local PDF templates via /product-mcp)
---

# ProductPilot 演示文稿生成与风格校准专家 (product-mcp)

本技能用于将产品方案、研究报告或规划思路，转化为高品质、符合业务线历史风格的 PPT 演示文稿结构与详细文案。

## 1. 适用场景
* 快速根据本地 PPT/PDF 模版风格提取排版规律。
* 编写符合 L1-L6 文字层级、客观无营销词的产品评审、管理层汇报幻灯片。

## 2. 核心工作流与多 Agent 协同机制 (Orchestration)
当用户使用 `/product-mcp` 唤醒此技能，或要求您按本地模版生成 PPT 时，AI 助手将自动拆分为 4 个协同角色依次执行任务：

### 🛠️ 1. 行业研究 (Research Agent)
* **核心职责**：通过自动检索本地文档，获取准确的现状背景数据。
* **执行动作**：自动在 Workspace 检索与课题相关的文档，提取痛点、工时、技术数据，为后续幻灯片提供坚实、详细的数据支撑。

### 🛠️ 2. 产品逻辑 (PM Agent)
* **核心职责**：提炼幻灯片整体骨架与 SCQA 故事线。
* **执行动作**：
  - 运用麦肯锡 **SCQA** 逻辑（背景 Situation → 冲突 Conflict → 疑问 Question → 回答 Answer）构建具有强说服力故事线。
  - 遵循**金字塔原理**（结论先行，以上统下，逻辑递进）。

### 🛠️ 3. 文案细化 (Copywriter Agent)
* **核心职责**：将逻辑骨架扩展为每个页面的 L1-L6 极其详细的文案内容，禁止一句话简单带过要点。
* **执行动作**：严格遵守 L1-L6 层级控制，L4 要点控制在 12-25 字并填充充分的技术与研究数据。

### 🛠️ 4. 视觉呈现 (UI/UX Agent)
* **核心职责**：配图生图，并套用 TCL 经典模板进行单文件自包含 HTML 代码生成。
* **执行动作**：
  - 自动调用 `generate_image` 生图工具在本地生成高品质图片（存入 `assets/images/`），绝不留白。
  - **视觉锁**：HTML 网页幻灯片在 DOM 和 CSS 上**必须 100% 保持 TCL 官方经典白底红标风格**，禁止擅自改动样式。
  - **扁平化结构**：严禁在内容页使用 `.slide-body` 嵌套层，所有页面核心元素必须作为 `.slide` 容器的直系子元素。

## 3. HTML 网页幻灯片布局限制与自适应规范 (HTML Slides Layout Guidelines)
* **3.1 扁平化 DOM 结构限制 (Don'ts)**：
  - **禁止引入全局包裹器**：在普通内容页（`.slide` 容器）内部，**严禁**引入 `<div class="slide-body">`、`<div class="wrapper">` 等嵌套层。这会导致 Flexbox 的垂直 `space-between` 空间分配机制完全失效，产生内容整体下移和上部大片空白的排版故障。
  - **组件平铺原则**：页面的所有核心逻辑大块（如 `slide-header`、`section-banner`、`grid-x-col`、`slide-footer`）**必须直接作为 `.slide` 容器的直系子元素 (Direct Children)**。
* **3.2 容器高度与拉伸规范 (Do's)**：
  - **内部高度自适应**：在直系子元素（如卡片组 `.grid-4-col`）内部放置子卡片时，子卡片的高度建议设置为 `height: 100%` 或 `flex-grow: 1`，以保证垂直方向自动拉伸整齐。
  - **间距留白限制**：严禁在直系子元素上随意使用大数值的 `margin-top`、`padding-top`。所有的垂直分布和留白应完全交由父级容器的 `justify-content: space-between` 自动计算分发。
  - **900px 垂直高度防溢出条件**：单页中所有直系子元素的高度（包括 margins 和 paddings）累加**不得超过 900px**。这能确保在 16:9 画布（高 1080px）内即使在不同分辨率下，底部的页脚和核心内容也绝不会因高度溢出而被截断。
