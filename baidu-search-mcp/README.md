# Baidu Search MCP Server

这是一个用于 Model Context Protocol (MCP) 的百度搜索服务器实现，它允许AI助手使用百度文心API进行智能搜索。

## 功能特性

- 支持使用百度文心API进行智能搜索
- 支持多种模型选择（ernie-3.5-8k, ernie-4.0-8k, deepseek-r1, deepseek-v3）
- 提供搜索结果和参考来源
- 支持深度搜索和时效性过滤

## 安装

```bash
npm install @modelcontextprotocol/sdk axios
```

## 配置

1. 首先需要获取百度文心API密钥：
   - 访问 [百度智能云](https://cloud.baidu.com/)
   - 创建应用并获取API密钥

2. 设置环境变量：

```bash
export BAIDU_API_KEY=your_api_key_here
```

## 使用方法

### 作为独立服务器运行

```bash
node build/index.js
```

### 在MCP配置中使用

在你的MCP设置文件中添加以下配置：

```json
{
  "mcpServers": {
    "baidu-search": {
      "command": "node",
      "args": ["/path/to/baidu-search-mcp/build/index.js"],
      "env": {
        "BAIDU_API_KEY": "your_api_key_here"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## API

### baidu_search

搜索工具支持以下参数：

- `query` (必需): 搜索查询文本
- `model`: 使用的模型名称
  - 可选值: "ernie-3.5-8k", "ernie-4.0-8k", "deepseek-r1", "deepseek-v3"
  - 默认值: "ernie-3.5-8k"
- `search_mode`: 搜索模式
  - 可选值: "auto", "required", "disabled"
  - 默认值: "auto"
- `enable_deep_search`: 是否开启深度搜索（默认：false）
- `search_recency_filter`: 搜索结果的时效性范围
  - 可选值: "week", "month", "semiyear", "year"

## 开发

1. 克隆仓库
2. 安装依赖：
```bash
npm install
```
3. 编译TypeScript：
```bash
npm run build
```

## 许可证

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 免责声明

本项目不对API密钥的使用承担责任，请确保遵守百度文心API的使用条款和政策。
