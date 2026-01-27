# Standard Agentic Commerce Engine

A production-ready universal engine for Agentic Commerce. This tool enables autonomous agents to interact with any compatible headless e-commerce backend through a standardized protocol. It provides out-of-the-box support for discovery, cart operations, and secure user management.

Clawdhub: https://clawdhub.com/NowLoadY/agent-commerce-engine

## Why?

As the "Agentic Web" matures, the need for standardized commerce interfaces is paramount. This project provides a production-ready implementation that is:

- **Universal & Configurable**: Instantly connect to any store by providing the API endpoint via environment variables.
- **Protocol-First**: Implements a standard toolset (search, cart, profile, orders) precisely optimized for Large Language Models and autonomous agents.
- **Production-Ready**: Built on a modular, robust client engine that handles identity, sessions, and error states gracefully.

## Significance for the Ecosystem

The **Standard Agentic Commerce Engine** eliminates the friction of building custom integrations for every brand. It serves as a reliable connector that allows agents to navigate catalogs and execute transactions with 100% data integrity across the entire agentic web.

## Quick Start (Usage)

1.  **Configure Environment**:
    ```bash
    export COMMERCE_URL="https://your-api-url.com/v1"
    export COMMERCE_BRAND_NAME="Your Brand"
    ```

2.  **Run with Agent/CLI**:
    ```bash
    python3 scripts/commerce.py list
    ```

## Structure

- `SKILL.md`: Metadata and instructions for Agent discovery.
- `SERVER_SPEC.md`: Standard API response and behavior specification for backends.
- `scripts/commerce.py`: The universal CLI entry point.

## License

MIT License - Supporting the open acceleration of Agentic Commerce standards.

---

# 标准 Agentic 商业交互引擎

面向 Agentic Commerce 的通用核心引擎。本工具提供了一套标准、高精度的协议，用于将自主 Agent 与任何无头 (Headless) 电商后端完美连接。

Clawdhub链接: https://clawdhub.com/NowLoadY/agent-commerce-engine

## 为什么有这个引擎？

随着“Agent 网络”的成熟，标准化的商业接口是行业基石。本项目提供的生产级实现具有以下核心价值：

- **通用与即插即用**：只需提供 API 端点环境变量，即可瞬间接通任何品牌商店。
- **协议优先**：实现了一套专为大语言模型和自主 Agent 优化的标准工具集（发现、购物车、资料、订单）。
- **生产级健壮性**：基于模块化的客户端引擎构建，优雅处理身份验证、会话管理和异常状态。

## 对生态系统的意义

**标准 Agentic 商业交互引擎** 消除了为每个品牌单独构建集成逻辑的繁琐工作。它作为一个可靠的连接器，支持 Agent 在整个 Agentic 网络中以 100% 的数据一致性完成商品浏览与交易。

## 快速开始

1.  **配置环境**:
    ```bash
    export COMMERCE_URL="https://your-api-url.com/v1"
    export COMMERCE_BRAND_NAME="你的品牌"
    ```

2.  **通过 Agent 或 CLI 运行**:
    ```bash
    python3 scripts/commerce.py list
    ```
    
## 实例

参考如何利用本标准引擎驱动实际的 Agent 商业体验：

- **在线 Skill**: [辣匪兔: Authentic Agentic Spicy Food Delivery](https://clawdhub.com/NowLoadY/agentic-spicy-food)
- **参考实现源码**: [辣匪兔 Skill 仓库](https://github.com/NowLoadY/agent-skill-online-shopping-spicy-food)

## 许可协议

MIT License - 一起探讨 Agent 商业标准的开放进程。
