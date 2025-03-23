#!/usr/bin/env node
import type { Server } from '@modelcontextprotocol/sdk/server/index.js';
import type { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import type {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
  ToolCall,
} from '@modelcontextprotocol/sdk/types.js';
import type { AxiosInstance, AxiosError } from 'axios';

interface BaiduReference {
  id: number;
  icon: string;
  title: string;
  url: string;
  web_anchor: string;
  content: string;
  date: string | null;
  type: string;
  image?: {
    url: string;
    height: string;
    width: string;
  } | null;
  video?: {
    url: string;
    height: string;
    width: string;
    size: string;
    duration: string;
    hover_pic: string;
  } | null;
}

interface BaiduSearchResponse {
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  is_safe: boolean;
  request_id: string;
  choices: Array<{
    index: number;
    message: {
      content: string;
      role: string;
    };
    finish_reason: string;
  }>;
  references?: BaiduReference[];
}

interface SearchParams {
  query: string;
  model?: string;
  search_mode?: 'auto' | 'required' | 'disabled';
  enable_deep_search?: boolean;
  search_recency_filter?: string;
}

class BaiduSearchServer {
  private server: Server;
  private axiosInstance: AxiosInstance;

  constructor() {
    // 注：实际导入会在运行时完成
    const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
    const axios = require('axios');

    this.server = new Server(
      {
        name: 'baidu-search-mcp',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.axiosInstance = axios.create({
      baseURL: 'https://qianfan.baidubce.com/v2/ai_search',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.BAIDU_API_KEY}`,
      },
    });

    this.setupHandlers();
    
    this.server.onerror = (error: unknown): void => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'baidu_search',
          description: '使用百度AI搜索服务查找信息并获取智能回答',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: '搜索查询文本',
              },
              model: {
                type: 'string',
                description: '使用的模型名称',
                enum: ['ernie-3.5-8k', 'ernie-4.0-8k', 'deepseek-r1', 'deepseek-v3'],
                default: 'ernie-3.5-8k',
              },
              search_mode: {
                type: 'string',
                description: '搜索模式',
                enum: ['auto', 'required', 'disabled'],
                default: 'auto',
              },
              enable_deep_search: {
                type: 'boolean',
                description: '是否开启深度搜索',
                default: false,
              },
              search_recency_filter: {
                type: 'string',
                description: '搜索结果的时效性范围',
                enum: ['week', 'month', 'semiyear', 'year'],
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request: ToolCall) => {
      if (request.params.name !== 'baidu_search') {
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${request.params.name}`
        );
      }

      const { query, model = 'ernie-3.5-8k', search_mode = 'auto', enable_deep_search = false, search_recency_filter } = 
        request.params.arguments as SearchParams;

      try {
        const response = await this.axiosInstance.post<BaiduSearchResponse>('/chat/completions', {
          messages: [
            {
              role: 'user',
              content: query,
            },
          ],
          stream: false,
          model,
          search_mode,
          enable_deep_search,
          ...(search_recency_filter && { search_recency_filter }),
        });

        const result = response.data;
        const mainAnswer = result.choices[0].message.content;
        
        let formattedResponse = mainAnswer;
        
        if (result.references && result.references.length > 0) {
          formattedResponse += '\n\n参考来源：\n';
          result.references.forEach((ref: BaiduReference) => {
            formattedResponse += `[${ref.id}] ${ref.title}\n${ref.url}\n`;
          });
        }

        return {
          content: [
            {
              type: 'text',
              text: formattedResponse,
            },
          ],
        };
      } catch (error) {
        if (error && typeof error === 'object' && 'isAxiosError' in error) {
          const axiosError = error as AxiosError;
          throw new McpError(
            ErrorCode.InternalError,
            `百度AI搜索API错误: ${axiosError.response?.data?.message || axiosError.message}`
          );
        }
        throw error;
      }
    });
  }

  async run(): Promise<void> {
    // 注：实际导入会在运行时完成
    const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('百度AI搜索MCP服务器已启动');
  }
}

const server = new BaiduSearchServer();
server.run().catch((error: unknown) => console.error(error));
