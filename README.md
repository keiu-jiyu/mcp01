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

需要我修改什么吗？
