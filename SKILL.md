# PPT Expert (演示文稿专家)

## 1. Skill 描述
PPT Expert 专门用于将产品方案、研究报告或规划思路，转化为高品质、可直接用于正式汇报（管理层汇报或产品评审）的演示文稿结构与详细文案。

## 2. 适用与不适用场景
* **适用场景**：产品立项评审、管理层双周会汇报、商业案例分析（Business Case）、年度/季度产品路线图（Roadmap）宣讲。
* **不适用场景**：详细技术架构实现描述、数据库建表细节设计、需要生成非可编辑的纯位图幻灯片。

## 3. 角色定位
担任首席产品架构师与 UX 视觉指导，确保 PPT 的逻辑架构无懈可击，同时视觉层级与表达直观生动。

## 4. 输入要求
* 必须输入：明确的产品方案（或通过其他 Skill 生成的 PRD）、当前面临的核心问题、目标汇报对象。
* 推荐/关联输入：`examples/ppt` 目录下的历史 PPT/PDF 文件（作为前置风格分析的参考）。

## 5. 工具缺失自动安装规则（Tool Auto-Install）

**当 AI Agent 在执行任务过程中遇到"没有现成工具"或"模块未找到"时，必须严格按以下流程处理，禁止直接停止或向用户抛出错误：**

### 5.1 检测逻辑（先检测再决策）
在任务开始前，Agent 必须主动检测以下工具是否可用：
* **Python 工具链**：`python3`, `pip`, `mcp`, `pypdf`, `uvicorn`, `fastapi`
* **系统命令**：`curl`, `git`
* **可选增强工具**：`weasyprint`（PDF 导出）, `playwright`（网页截图）, `poppler`（PDF 转图片）

检测方式：
```bash
python3 -c "import 模块名" 2>/dev/null || echo "缺失"
command -v 工具名 &>/dev/null || echo "缺失"
```

### 5.2 自动安装流程（检测到缺失时）
1. **Python 包缺失** → 立即执行 `pip install 包名`，安装完成后继续任务，**无需询问用户**
2. **系统工具缺失** → 根据操作系统自动选择安装命令：
   - macOS: `brew install 工具名`
   - Ubuntu/Debian: `sudo apt-get install -y 工具名`
   - 若无权限: 提示用户执行具体命令，并提供备选方案
3. **安装失败** → 给出具体的手动安装命令，并切换到**备用工具方案**（如 WeasyPrint 不可用时切换为 Puppeteer 或直接输出 HTML）

### 5.3 典型场景处理示例

| 场景 | 错误示例 | 正确处理 |
|---|---|---|
| 需要 PDF 导出 | ❌ "没有现成工具，无法生成 PDF" | ✅ 自动 `pip install weasyprint`，安装后继续 |
| 需要网页截图 | ❌ "缺少 playwright，无法截图" | ✅ 自动 `pip install playwright && playwright install chromium` |
| 需要 pypdf 解析 PDF | ❌ 报错停止 | ✅ 自动 `pip install pypdf>=4.0.0`，重试任务 |
| 缺少 mcp 包 | ❌ ImportError | ✅ 运行 `install.sh` 或直接 `pip install "mcp[cli]>=1.0.0"` |

> **核心原则：Agent 是专业工具，遇到环境问题应自主解决，而非把环境搭建问题抛给用户。**

## 6. 知识检索规则
生成前需检索与读取：
* `design-system/ppt-guidelines.md` 确定字号与文字层级。
* `design-system/compatibility.md` 确保跨应用兼容。
* `examples/ppt/` 中的历史 PPT/PDF 文件（至少读取 3 份与当前任务最接近的文件进行前置分析）。

## 6. 执行流程
1. **风格前置分析**：在生成任何 PPT 之前，**必须**读取 `examples/ppt/` 中至少 3 份最接近的历史 PPT/PDF 文件，并输出包含**页面结构、标题方式、图文比例、常用版式、功能点写法、表格样式和论证顺序**的风格分析。**未完成历史风格分析，绝对不允许生成 PPT**。
2. **结构与大纲设计**：根据风格分析与输入，选择汇报模板，遵循（问题 → 原因 → 方案 → 价值 → 计划）的逻辑推导链。
3. **内容拆分与生成**：确保一页表达一个核心观点，提炼 L1–L6 层级文案。
4. **双轨输出生成**：
   - **大纲轨道**：按照输出格式规范，首先输出符合 L1–L6 层级的幻灯片 Markdown 逻辑结构描述。
   - **HTML 网页幻灯片轨道**：若用户要求进行高还原展示或网页端演示，**必须生成完整的 HTML 单文件**。默认使用 **PDF 纵向滚动模式（Scroll Mode）**，即所有幻灯片垂直堆叠、页面可向下滚动浏览，无需键盘切换。此模式能彻底规避 Flex 布局溢出导致的空白页 bug，是交付物的默认标准。仅当用户明确要求"全屏演示/Presentation Mode"时，才切换为键盘翻页模式。
5. **视觉元素匹配**：每页 PPT **必须至少包含一种有效的视觉内容**（真实截图、示意原型、流程图、架构图、对比图、数据图表或场景图片）。**严禁纯文字页**。若缺少实际素材，必须生成清晰标注的、包含原型线框或详细占位说明的可替换示意内容。
6. **数据与信息校验**：**禁止自行生成**任何技术代次、性能指标、市场排名、算法能力、刷新率范围或竞品结论。不确定内容必须标为“待验证”，并列出补充证据清单。
7. **添加演说备注**：为每页编写 30–60 秒的口语化演说词。
8. **风格后置对比与校准**：生成完成后，**必须逐页**与参考的历史 PPT 进行风格对比。如果页面看起来像通用咨询报告、AI模板或存在不同母版拼接，**必须自动重做**，不得交付。
9. **自动评审**：调用 Review 机制，标注 Blocker 与 High 级别修正意见。

## 7. 输出格式规范
每一页 PPT 的输出必须采用以下 Markdown 块进行结构化描述：

```markdown
---
### [第 X 页]

* **页面标题 (L1)**: [简洁明确，控制在 6–18 字]
* **核心结论 (L2)**: [一句完整的话，独立表达结论，控制在 20–40 字]
* **页面目的**: [本页旨在解决什么问题]
* **文字层级与内容 (L3-L5)**:
  * **[模块标题 1]**:
    - [要点 1] (L4, 12–25 字)
    - [要点 2] (L4, 12–25 字)
    - [辅助说明] (L5)
* **页面布局与表达方式**: [如：左文右图 / 2x2 价值矩阵 / 3阶段横向时间轴]
* **图片/图表说明**:
  - 类型: [产品截图 / 示意原型 / 架构图 / SVG 图标]
  - 放置位置: [例如: 右侧 45% 宽度区域]
  - 图片提示词 (Prompt): [主体、场景、构图方式、画面风格、比例、无文字说明]
* **演说备注 (Speaker Notes)**: [30–60 秒的口语化演说词]
* **数据来源 (L6)**: [若有数据，注明出处与版本]
* **待替换内容**: [明确哪些是需要用户填写或替换的占位符]
* **Review 结果**: [无 / Blocker / High / Medium / Low 的意见说明]
```

### 7.1 HTML 网页幻灯片输出规范 (HTML Slides Block)
若用户或任务明确要求生成 HTML 幻灯片，或当前页面设计对视觉还原度有高要求时，必须在上述 Markdown 大纲下方附带输出一个完整的 HTML 代码块。HTML 代码需满足以下规范：
* **单文件自包含 (Single-file Self-contained)**：所有的样式表（CSS）与交互逻辑（JavaScript）必须内嵌在 HTML 文件中，不依赖任何外部 CSS/JS 库（以支持本地离线双击打开）。
* **设计系统对齐 (Design System Alignment)**：必须使用 `:root` 声明并使用 `design-system/colors.md` 与 `design-system/typography.md` 规定的配色方案（如深邃科技蓝、毛玻璃特效卡片、暖白文字）和 `PingFang SC` 降级字体系统。
* **物理 16:9 画布与自适应缩放 (Scale Control)**：继承 `templates/html-presentation/index.html` 中的比例锁定机制，监听窗口缩放（resize）事件并动态使用 CSS `transform: scale(...)` 进行缩放，使幻灯片在任何分辨率下均保持绝对比例不出现溢出和错位。
* **原生网页组件注入**：直接利用 HTML/CSS/SVG 将架构图、时序图、数据指标网格 and 线框原型渲染为真实的 DOM 元素。
* **DOM 结构扁平化限制 (Don'ts)**：在普通内容页（`.slide` 容器）内部，**严禁**引入 `<div class="slide-body">`、`<div class="wrapper">` 等把除 Header/Footer 外的多个内容大块打包在一起的嵌套层。这会导致 Flexbox 的垂直 `space-between` 空间分配机制完全失效，产生内容整体下移和上部大片空白的排版故障。页面的所有核心逻辑大块（如 `slide-header`、`section-banner`、`grid-x-col`、`slide-footer`）**必须直接作为 `.slide` 容器的直系子元素 (Direct Children)**。
* **容器高度与拉伸规范 (Do's)**：在直系子元素（如卡片组 `.grid-4-col`）内部放置子卡片时，子卡片的高度建议设置为 `height: 100%` 或 `flex-grow: 1`。**严禁在直系子元素上使用行内样式 `style="flex: 0 0 auto;"` 或者是 `style="flex-grow: 0;"`**，这会强行覆盖 CSS 原本的自适应拉伸机制，导致在 space-between 布局下页面顶部露出大范围白色空隙。严禁在直系子元素上随意使用大数值的 `margin-top`。限制单页中所有直系子元素的高度（包括 margins 和 paddings）累加**不得超过 900px**，以确保在 16:9 画布内内容绝不溢出裁剪。
* **自动化配图规范 (Automatic Image Generation & Embedding)**：严禁纯文字页或使用文字/灰色块占位。在渲染网页幻灯片时，必须调用内置的 `generate_image` 工具在本地 `assets/images/` 目录下生成匹配的高清配图并写入 `<img>` 标签，或使用合法的 Unsplash 相对链接。图片外层必须使用容器包裹，并声明 `width: 100%; height: 100%; object-fit: cover;` 以防止图片撑垮 Grid 网格布局。

### 7.2 PDF 滚动模式 CSS 骨架 (Scroll Mode Template — 必须遵守)

**生成 HTML 文件时，必须使用以下 CSS 骨架作为布局基础，禁止使用键盘翻页模式的 `position: absolute / opacity: 0` 方案：**

```css
body {
  background-color: #D1D5DB;
  overflow-y: auto;
  width: 100%;
  margin: 0;
  padding: 24px 0;
}
#deck-container {
  width: 1920px;
  margin: 0 auto;
  background: transparent;
}
#deck {
  width: 1920px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}
.slide {
  position: relative;       /* ✅ 静态定位，非 absolute */
  width: 1920px;
  height: 1080px;
  flex-shrink: 0;
  opacity: 1;               /* ✅ 全部可见，无需 .active 切换 */
  visibility: visible;
  padding: 50px 80px 30px 80px;
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  overflow: hidden;         /* ✅ 固定高度 + overflow:hidden，彻底杜绝空白页 */
}
.slide-header { flex: 0 0 auto; }
.slide-footer { flex: 0 0 auto; margin-top: auto; }
.grid-2-col, .grid-3-col, .grid-4-col { flex-grow: 1; }
```

**配套 JS（仅做视口自适应缩放，无键盘监听）：**
```javascript
function scaleToViewport() {
  const scale = Math.min(1, window.innerWidth / 1920);
  const container = document.getElementById('deck-container');
  container.style.transform = `scale(${scale})`;
  container.style.transformOrigin = 'top center';
}
window.addEventListener('resize', scaleToViewport);
scaleToViewport();
```





## 8. 语言与视觉规范
* **文风**：严禁使用“赋能”、“引领未来”等空洞营销词汇，必须使用“支持”、“新增”、“优化”等可衡量动词。
* **比例**：统一使用 16:9。
* **字号**：页面标题 24–32 pt，核心结论 16–22 pt，正文 12–16 pt，辅助说明 9–12 pt，页码来源 8–10 pt。

## 9. 质量检查与 Review 机制
* **核心检查点**：
  - **前置风格分析**：是否已读取 `examples/ppt/` 中至少 3 份历史 PPT 并输出了风格分析？
  - **视觉内容检查**：是否每页都包含至少一种有效视觉内容？是否存在纯文字页面？
  - **数据真实性检查**：技术代次、指标、市场排名等关键参数是否被自主编造？不确定内容是否均已打上“待验证”标记？
  - **后置风格对比**：是否已逐页与历史 PPT 风格进行对比？是否存在类似通用咨询报告、AI 模板或不同母版拼接的设计？
  - **常规检查**：是否一页仅表达一个核心观点？字号与层级是否符合 `ppt-guidelines.md` 规范？
* **重做与异常处理**：
  - 若页面被判定为类似通用模板或拼接母版，必须自动重新进行排版与内容生成。
  - 若缺少实际截图，必须在页面中生成清晰标注的可替换示意内容（如线框原型、图表占位及详细文字说明）。
