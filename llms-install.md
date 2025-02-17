# DeepClaude MCP (Model Control Panel)

[English](./README.md) | [中文](./README_CN.md)

## Overview
DeepClaude MCP (Model Control Panel) is a powerful server application that combines the capabilities of DeepSeek and Claude AI models to deliver enhanced results. This integration allows for more accurate and comprehensive AI responses by leveraging the strengths of both models.

## Features
- Seamless integration of DeepSeek and Claude AI models
- RESTful API endpoints for easy integration
- Configurable model parameters
- Robust error handling with Winston logger
- Cross-origin resource sharing (CORS) support
- TypeScript implementation for type safety

## Prerequisites
- Node.js (v14 or higher)
- npm or yarn package manager
- API keys for both DeepSeek and Claude services

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Mrdapeng/DeepClaudeMcp.git
cd DeepClaudeMcp
```

2. Install dependencies:
```bash
yarn install
# or
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

## Development
- Start development server with hot-reload:
```bash
yarn dev
# or
npm run dev
```

- Build the project:
```bash
yarn build
# or
npm run build
```

- Start production server:
```bash
yarn start
# or
npm start
```

## Project Structure
```
src/
├── config/     # Configuration files
├── services/   # Core services and API clients
├── types/      # TypeScript type definitions
└── index.ts    # Application entry point
```

## Dependencies
- Express.js - Web framework
- Axios - HTTP client
- Winston - Logging library
- CORS - Cross-origin resource sharing
- dotenv - Environment configuration
- TypeScript - Programming language
- Jest - Testing framework

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```
