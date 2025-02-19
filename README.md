# MCP Marketplace

Welcome to Cline's **MCP Marketplace** repository! Submit your MCP servers for others to easily discover and one-click install with Cline.

## Table of Contents

1. [What is MCP?](#what-is-mcp)
2. [What is the MCP Marketplace?](#what-is-the-mcp-marketplace)
3. [How to Submit your MCP Server](#how-to-submit-your-mcp-server)
4. [Making Your MCP Server One-Click Installable](#making-your-mcp-server-one-click-installable)
5. [FAQ](#faq)
6. [Get Help](#get-help)

## What is MCP?

**[MCP](https://github.com/modelcontextprotocol) (Model Context Protocol)** is an open protocol introduced by Anthropic that standardizes how large language models communicate with external tools or resources. MCP servers allow AI agents like Cline to access additional capabilities e.g., web search, file operations, API integrations, database access, and more.

## What is the MCP Marketplace?

The MCP Marketplace is a curated collection of MCP servers that makes discovery and installation easy. With the marketplace, you can:

1.  Browse official and community-made MCP servers
2.  Search by name, category, tags, and other metadata
3.  Install MCP servers with one click, triggering Cline to autonomously handle cloning, setup, and configuration.

## How to Submit your MCP Server

1. Create a [new issue](https://github.com/cline/mcp-marketplace/issues/new) in this `mcp-marketplace` repository
2. **Include the Following Info** in the Issue:
    - **GitHub Repo URL:** A direct link to the MCP server’s repository (nested links are also okay like in this [example](https://github.com/modelcontextprotocol/servers/tree/main/src/github))
    - **Logo Image:** A 400×400 PNG that will serve as your server’s icon.
    - **Reason for Addition:** Briefly explain why your server is awesome and/or how it can benefit other Cline users.
3. Confirm that you have tested giving Cline just your `README.md` and/or the `llms-install.md` and watched him successfully setup the server. This will save our reviewers a lot of time manually setting up servers prior to approval.

That’s it! Our team will review your submission. Once approved, we’ll add your MCP server to the official Marketplace listings, and it will become discoverable by Cline users.

## Making Your MCP Server One-Click Installable

When Cline attempts to install your MCP server, he will try to use your `README.md` to guide him through the setup process. While most MCP servers include sufficient instructions in their README, you can include a `llms-install.md` file in your repository to provide additional guidance to agents like Cline. This can be particularly useful for complex setups requiring specific environment configurations or API keys.

## FAQ

1.  **Do I have to create a `llms-install.md` file?**
    No. A well-written README with clear installation instructions is usually sufficient. Cline is quite good at understanding standard README files. The `llms-install.md` file is optional to help with complex setups or when you want to provide additional guidance.
2.  **Can I submit new MCP servers without many stars?**
    Absolutely! However, we do have a vetting process to ensure the security and stability of the MCP ecosystem.
3.  **How long does the approval process take?**
    Our team aims to review submissions within a couple of days. If your submission is approved, it will be live in the marketplace shortly thereafter.

## Get Help

Join our [Discord](https://discord.gg/cline) and post in the `#mcp` channel if you have any questions or need help!

## License

This repository is distributed under the [MIT License](LICENSE). Please note that individual MCP server submissions may use different licenses, so review the original repo’s license for details.
