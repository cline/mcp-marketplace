# MCP Marketplace

Welcome to the **MCP Marketplace** repository! This is where anyone can submit their MCP (Model Context Protocol) servers for seamless integration with Cline. Once approved, your server will be listed in Cline’s MCP marketplace, enabling millions of people to discover, install, and configure MCP servers with minimal friction.

## Table of Contents

1.  [What is MCP?](#what-is-mcp)
2.  [What is the MCP Marketplace?](#what-is-the-mcp-marketplace)
3.  [When Should I Use `llms-install.md`?](#when-should-i-use-llms-installmd)
4.  [Submission Requirements](#submission-requirements)
5.  [How to Submit your MCP Server](#how-to-submit-your-mcp-server)
6.  [Making Your MCP Server Installation-Friendly](#making-your-mcp-server-installation-friendly)
7.  [Best Practices for `llms-install.md`](#best-practices-for-llms-installmd)
8.  [Example `llms-install.md` Structure](#example-llms-installmd-structure)
9.  [FAQ](#faq)
10.  [Get Help](#get-help)
11.  [License](#license)

## What is MCP?

**MCP (Model Context Protocol)** is an open protocol introduced by Anthropic that standardizes how large language models communicate with external tools or resources. MCP servers allow AI agents to access additional tools and capabilities through a standardized protocol developed by Anthropic. For example, an MCP server could enable:

- Web search capabilities 
- File operations
- API integrations (Figma, GitHub, etc)
- Database access
- And more...

## What is the MCP Marketplace?

The **MCP Marketplace** is akin to an “app store” within Cline's VS Code extension. It lets you:

1.  Browse a list of popular or community-created MCP servers.
2.  Search by name, category, tags, and other metadata.
3.  Install MCP servers with one click, triggering Cline to autonomously handle cloning, setup, and configuration.
4.  Configure any required API keys or preferences on the fly, guided by Cline.

## When Should I Use `llms-install.md`?

The key to a successful MCP server is clear, detailed installation instructions that both humans and AI agents can follow. Most well-written README files already do this job perfectly! Cline is quite good at understanding standard README files and can successfully install most MCP servers using just the README.

For complex setups or when you want to provide additional AI-specific guidance, you can optionally create a separate `llms-install.md` file. This dedicated file lets you include extra context or more explicit instructions specifically formatted for AI agents, without cluttering your main README.

When Cline attempts to install your MCP server, he will:
1. Check for installation instructions in your README
2. If present, also consider any additional guidance in `llms-install.md`

**Key goals:**

*   Provide an AI agent with all the context it needs (dependencies, steps, environment variables, etc.)
*   Clarify any optional vs. required API keys and how they should be used.
*   Reduce user frustration by minimizing guesswork the AI would otherwise have to do.

## Submission Requirements

When you’re ready to add your MCP server to the Marketplace, please ensure you have:

1.  **A GitHub Repository** containing your MCP server implementation.
2.  **A 400×400 PNG Image** to represent your MCP server in the Marketplace UI.
3.  **A short justification** (a sentence or two) describing why you think your MCP server belongs in the Marketplace.
4.   **Clear installation instructions** in your README. Optionally, you can also include a `llms-install.md` file for additional AI-specific guidance.

## How to Submit your MCP Server

1. Create a [new issue](https://github.com/cline/mcp-marketplace/issues/new) in this `mcp-marketplace` repository
2.  **Include the Following Info** in the Issue:
    *   **GitHub Repo URL:** A direct link to the MCP server’s repository (nested links are also okay like in this [example](https://github.com/modelcontextprotocol/servers/tree/main/src/github))
    *   **Logo Image URL:** A link to a 400×400 PNG that will serve as your server’s icon.
    *   **Reason for Addition:** Briefly explain why your server is awesome and/or how it can benefit other Cline users.
3.  Confirm that you have tested giving Cline just your `README.md` and/or the `llms-install.md` and watched him successfully setup the server. This will save our reviewers a lot of time manually setting up servers prior to approval.

That’s it! Our team will review your submission. Once approved, we’ll add your MCP server to the official Marketplace listings, and it will become instantly discoverable by Cline users.

We review all submissions to ensure quality, **seamless installation**, and compatibility. So please make sure you provide enough information in your `README.md` and `llms-install.md` for Cline to be able to set up your server all on his own.

## Making Your MCP Server Installation-Friendly

While not required, you can include a `llms-install.md` file in your repository. This file helps AI agents like Cline reliably install your MCP server by providing clear, structured installation instructions.

The standard `README.md` works great for humans, but `llms-install.md` can be more explicit for AI agents to understand installation and api key requirements.

### Best Practices for `llms-install.md`

1.  **Keep It Step-by-Step**
    *   Use bullet points or numbered lists for each part of the installation process.
    *   Be explicit about commands, file paths, and environment variables.
2.  **Describe Platform Requirements**
    *   Call out dependencies like Python, Node.js, or Go versions.
    *   Specify if you need Docker or any other containerization.
3.  **Clarify API Keys**
    *   Which APIs are required?
    *   How do you obtain an API key?
    *   Which APIs are optional, and what extra features do they enable?
4.  **Offer Minimal External Links**
    *   The LLM may not always be able to open external documentation automatically.
    *   Include essential instructions in the file itself.
5.  **Use Plain Language**
    *   Keep your tone direct and explanatory. Avoid unnecessary jargon.
6.  **Include a Troubleshooting Section**
    *   Suggest ways to handle common errors (e.g., missing dependencies, invalid credentials).

## Example `llms-install.md` Structure

Below is a simplified example of what your `llms-install.md` might look like. Adapt as needed for your project.

```
# llms-install.md

## Overview
This guide helps an LLM agent install and configure the XYZ MCP Server.

## Steps

1. **Clone the Repo**
   - Command: `git clone https://github.com/username/xyz-mcp-server.git`
   - Install dependencies: `npm install` (for Node.js) or `pip install -r requirements.txt` (for Python), etc.

2. **Set Up Configuration**
   - Create a `.env` file (if required).
   - Include:
     ```
     API_KEY=
     OPTIONAL_FEATURE_FLAG=true
     ```

3. **Run the MCP Server**
   - Command: `npm start` or `python app.py`
   - The server listens on `localhost:8080` by default.

## API Keys
- **Required**: `API_KEY` from [provider.com](https://provider.com).
- **Optional**: `ANALYTICS_KEY` for advanced telemetry.

## Troubleshooting
- **Missing Dependencies**: Make sure `node --version` is at least 14.x or `python --version` is at least 3.8.
- **Permission Errors**: Run with elevated privileges or ensure the correct file permissions.
```

## FAQ

1.  **Do I have to create a `llms-install.md` file?**  
    No. A well-written README with clear installation instructions is usually sufficient. Cline is quite good at understanding standard README files. The `llms-install.md` file is an optional enhancement you can use for complex setups or when you want to provide additional AI-specific guidance.
2.  **Can I submit my MCP server if it’s still in alpha?**  
    Absolutely! We welcome all sorts of experiments and innovations. Just make sure users know about any instability or incomplete features.
3.  **How long does the approval process take?**  
    Our team aims to review submissions within a couple of days. If your submission is approved, it will be live in the marketplace shortly thereafter.

## Get Help

- Join our [Discord](https://discord.gg/cline) and post in the `#mcp` channel if you have any questions or need help!

## License

This repository is distributed under the [MIT License](LICENSE). Please note that individual MCP server submissions may use different licenses, so review the original repo’s license for details.

**Thank You!**  


