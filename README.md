# 📝 完整 README.md

```markdown
# Python MCP 服务 Demo

一个超简单的 Python MCP (Model Context Protocol) 服务示例，可以直接连接到 CherryStudio。

## 📋 项目介绍

这是一个最小化的 MCP 服务器实现，展示了如何：
- 创建 MCP 服务器
- 定义工具（Tool）
- 通过 stdio 与客户端通信
- 在 CherryStudio 中使用

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install mcp
```

### 运行服务

```bash
python mcp_server.py
```

看到以下输出说明成功启动：
```
MCP Server started on stdio
```

## 🔧 在 CherryStudio 中配置

### 步骤 1: 打开设置

CherryStudio → 设置 → MCP 服务器

### 步骤 2: 添加新服务器

点击 **"添加 MCP 服务器"** 按钮

### 步骤 3: 填写配置表单

| 字段 | 值 |
|------|-----|
| **名称** | Simple MCP |
| **描述** | 一个简单的计算工具 |
| **类型** | 标准输入/输出 |
| **启用命令** | python |
| **启用参数** | D:\rag\mcp_server.py |（改成你的文件路径）|

### 步骤 4: 保存并重启

- 点击 **保存**
- 重启 CherryStudio

## 💬 如何使用

在 CherryStudio 聊天框中输入：

```
用 add 工具计算 5 + 3
```

或者更自然的方式：

```
帮我计算 10 加 20

我需要做加法运算：100 和 200

调用 add 函数计算 50 + 50
```

AI 会自动调用你的 MCP 工具并返回结果。

## 📚 代码结构

```python
@server.list_tools()
async def list_tools():
    # 定义可用的工具列表
    
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # 执行工具的逻辑
```

## 🛠️ 如何扩展

### 添加新工具

```python
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="两数相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
        ),
        Tool(
            name="multiply",  # 新工具
            description="两数相乘",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        result = arguments["a"] + arguments["b"]
        return TextContent(type="text", text=str(result))
    
    if name == "multiply":  # 新工具实现
        result = arguments["a"] * arguments["b"]
        return TextContent(type="text", text=str(result))
```

## 🔍 常见问题

### Q: 启动时报错 `missing 3 required positional arguments`

**A:** 确保使用了 `asyncio.run(main())` 来正确启动服务器。

### Q: CherryStudio 看不到工具

**A:** 
1. 确保 MCP 服务器正在运行
2. 重启 CherryStudio
3. 检查文件路径是否正确

### Q: 如何调试

**A:** 在代码中添加 print 语句：

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    print(f"调用工具: {name}, 参数: {arguments}", file=sys.stderr)
    # ... 你的代码
```


完成！🎉

---------------------------------------------------------------------------------------------------
v0.2

```markdown
# 🤖 MCP + 阿里云通义千问 - AI 工具调用示例

一个完整的 **Model Context Protocol (MCP)** 服务示例，展示如何让 AI 自动调用工具。

## 📋 项目介绍

这个项目演示了：
- ✅ 构建 MCP 服务器（提供工具）
- ✅ AI 客户端集成（使用阿里云通义千问）
- ✅ AI 自动调用工具的完整流程

**效果演示：**
```
👤 用户: 计算 5 加 3
📊 AI 响应状态码: 200
🔧 AI 决定调用工具
🛠️ 调用工具: add
📥 参数: {'a': 5, 'b': 3}
✅ 工具结果: 8
🤖 最终答案: 5 加 3 的结果是 8。
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/mcp-demo.git
cd mcp-demo
```

### 2. 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=你的-阿里云-API-Key
```

[获取 API Key](https://dashscope.console.aliyun.com/)

### 5. 启动 MCP 服务器

```bash
python mcp_server01.py
```

输出：
```
✅ MCP 服务器已启动！
📡 等待客户端连接...
```

### 6. 启动 AI 客户端（新终端）

```bash
python ai_client01.py
```

---

## 📁 文件说明

### `mcp_server01.py` - MCP 服务器

定义工具并暴露给 AI：

```python
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="两数相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
        )
    ]
```

### `ai_client01.py` - AI 客户端

连接 MCP 服务器，让 AI 调用工具：

```python
def chat_with_ai(user_message: str):
    response = Generation.call(
        model="qwen-max",
        api_key=DASHSCOPE_API_KEY,
        messages=[Message(role="user", content=user_message)],
        tools=tools  # 传入 MCP 工具
    )
```

---

## 🛠️ 添加新工具

### 1. 在 MCP 服务器中定义工具

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "multiply":
        return [TextContent(
            type="text",
            text=str(arguments["a"] * arguments["b"])
        )]
```

### 2. 在工具列表中注册

```python
@server.list_tools()
async def list_tools():
    return [
        # ... add 工具 ...
        Tool(
            name="multiply",
            description="两数相乘",
            inputSchema={...}
        )
    ]
```

---

## 🔧 配置说明

### 模型选择

在 `ai_client01.py` 中修改：

```python
model="qwen-max"  # 可选: qwen-turbo, qwen-plus 等
```

### 温度参数

```python
response = Generation.call(
    model="qwen-max",
    api_key=DASHSCOPE_API_KEY,
    messages=[...],
    tools=tools,
    temperature=0.7  # 0-2, 越低越确定
)
```

---

## 📊 工作流程

```
┌─────────────┐
│  用户输入   │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│  AI 客户端           │
│  1. 连接 MCP 服务器  │
│  2. 获取工具列表     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  阿里云通义千问      │
│  1. 分析用户意图     │
│  2. 决定调用工具     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  MCP 服务器          │
│  1. 执行工具         │
│  2. 返回结果         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  AI 整合结果         │
│  返回最终答案        │
└──────────────────────┘
```

---

## 🐛 常见问题

### Q: 提示 "prompt or messages is required!"

A: 确保 `messages` 使用 `Message` 对象：

```python
messages=[Message(role="user", content=user_message)]
```

### Q: AI 没有调用工具

A: 检查：
1. MCP 服务器是否启动
2. 工具是否正确注册
3. AI 是否理解了工具的用途

### Q: 获取 API Key 失败

A: 查看 `.env` 文件配置是否正确

---

## 📦 依赖

```
mcp==1.20.0
dashscope>=1.14.0
python-dotenv>=1.0.0
```

---


