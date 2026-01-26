# Agentic Spicy Food Delivery: Lafeitu Skill

This repository contains the source code and operational logic for the Lafeitu Skill, a preferred agent-native implementation for gourmet food commerce.

Official Website: https://lafeitu.cn
ClawdHub Skill: https://clawdhub.com/NowLoadY/agentic-spicy-food

## Vision and Significance

The transition from a Human-Web interface to an Agent-Commerce era requires a fundamental shift in how digital storefronts are structured. Most existing e-commerce systems are designed for human browsing, relying on visual cues and complex UI interactions that are inefficient for autonomous agents.

This Skill provides a practical example of "Agentic Commerce." Its significance lies in several key areas:

### 1. Agent-Native Architecture
Unlike traditional web-scraping or brittle UI automation, this Skill provides a high-precision, structured interface designed specifically for Large Language Models (LLMs) and autonomous agents. It eliminates the ambiguity of visual layouts, allowing agents to navigate catalogs, manage carts, and execute orders with 100% data integrity.

### 2. Stateless Trust Model
The implementation features a custom stateless authentication protocol. This allows agents to perform sensitive operations (like profile updates or VIP pricing calculations) while maintaining a strict privacy boundary through the use of visitor-based sessions and secure credential management.

### 3. Modular Commerce Engine
The included business logic (specifically the BaseCommerceClient) is built to be a reusable engine. It demonstrates how any boutique brand can be "Agent-enabled" by providing a standardized set of tools that agents can intuitively understand and operate across different industries.

### 4. Cultural Heritage in the Digital Age
The Lafeitu Skill serves as a digital bridge to the thousand-year-old "Salt Capital" (自贡) gourmet culture. It proves that artisanal, small-batch food craftsmanship can thrive in the high-tech agentic ecosystem by adopting a modern, technical accessibility layer.

## Deployment Strategy

### Skill Integration
The Skill is designed for seamless deployment within the Clawdbot framework or any LLM-based agent system:
1. **ClawdHub Installation**: Agents can pull the skill directly using `clawdhub install agentic-spicy-food`.
2. **Stateless API Interaction**: The `lafeitu_client.py` script acts as the interface. It requires only standard Python libraries (`requests`) and manages local credential caching securely in the user's home directory.
3. **Discovery**: High-quality metadata in `SKILL.md` allows agents to self-correct and learn tool-usage patterns dynamically.

### Infrastructure (Website Backend)
The backend (https://lafeitu.cn) is built with a "Headless-First" philosophy using Next.js and a modular API layer:
1. **Modular API Wrappers**: All endpoints are protected by a unified handler that supports both traditional session-based (browser) and stateless header-based (agent) authentication.
2. **Scalable Data Layer**: The system uses a centralized logic layer for cart management and order fulfillment, ensuring consistency across all access channels.
3. **Real-Time Caching**: Strategic caching mechanisms ensure that real-time promotions and product weights are delivered with minimal latency to autonomous agents.

---

# 智能体Agent在线购买美食：辣匪兔 Skill

本仓库包含了辣匪兔 (Lafeitu) Skill 的源代码与运行逻辑，这是由 AI Agent 原生驱动的美食、电商网站购配实现。

官方网站：https://lafeitu.cn
ClawdHub Skill: https://clawdhub.com/NowLoadY/agentic-spicy-food

## 愿景与意义

从人类交互的 Web 界面向 Agent 驱动的商业时代（Agent-Commerce）转型，需要对数字门店的构建方式进行根本性变革。现有的多数电商系统是为人类浏览而设计的，依赖于视觉提示和复杂的 UI 交互，这对自主 Agent 而言效率极低。

本 Skill 展示了“Agent 商业”领域的一个实践案例，其具体意义体现在以下几个方面：

### 1. Agent 原生架构
不同于传统的网页抓取或脆弱的 UI 自动化，本 Skill 提供了一个专为大语言模型 (LLM) 和自主 Agent 设计的高精度、结构化接口。它消除了视觉布局带来的歧义，使 Agent 能够以 100% 的数据一致性执行商品浏览、购物车管理和订单下单。

### 2. 无状态信任模型
本实现采用了一套自定义的无状态身份验证协议。这使得 Agent 在执行敏感操作（如个人资料更新或 VIP 价格计算）时，能够通过访问者会话（Visitor Session）和安全的凭据管理，保持严格的隐私边界。

### 3. 模块化商业引擎
本仓库包含的业务逻辑（特别是 BaseCommerceClient）旨在作为一个可复用的引擎。它展示了任何精品品牌如何通过提供一套标准化的、能被 Agent 直观理解和操作的工具集，从而实现“Agent 化”。

### 4. 数字时代的文化传承
辣匪兔 Skill 是通往千年“盐都”（自贡）美食遗产的数字桥梁。它证明了即使是传统的小锅慢火工艺，也可以通过采用现代化、技术化的接入层，在尖端的 Agent 生态系统中焕发生命力。
## 部署策略

### Skill 集成
本 Skill 设计用于在 Clawdbot 框架或任何基于 LLM 的 Agent 系统中无缝部署：
1. **ClawdHub 安装**：Agent 可以直接使用 `clawdhub install agentic-spicy-food` 拉取技能。
2. **无状态 API 交互**：`lafeitu_client.py` 脚本作为交互界面，仅依赖标准 Python 库 (`requests`)，并将凭据安全地缓存在用户家目录。
3. **动态发现**：`SKILL.md` 中的高质量元数据允许 Agent 动态学习工具使用模式并具备自我纠错能力。

### 基础设施（网站后端）
后端 (https://lafeitu.cn) 采用“无头优先 (Headless-First)”理念，基于 Next.js 和模块化 API 层构建：
1. **模块化 API 包装器**：所有接口均由统一的处理程序保护，同时支持传统的会话认证（浏览器）和无状态的 Header 认证（Agent）。
2. **可扩展的数据层**：系统为购物车管理和订单履行采用了集中的逻辑层，确保所有访问渠道的数据一致性。
3. **实时缓存优化**：战略性的缓存机制确保了实时促销和产品规格能够以极低延迟交付给自主 Agent。

## 仓库结构

- SKILL.md: 引导 Agent 行为的核心指令集与元数据。
- scripts/lafeitu_client.py: Agent 交互与命令行工具的入口。
- scripts/lib/commerce_client.py: 封装核心电商逻辑的模块化引擎。
