# 🔓 Claude Code Rebuilt — 泄露源码完整复原版

> 基于 2026 年 3 月 31 日意外泄露的 Claude Code 源码，补全所有缺失部分后的可本地运行完整版本。

---

## 📖 背景

2026 年 3 月 31 日，Anthropic 在 npm 注册表中意外通过 source map 文件暴露了 [Claude Code](https://github.com/anthropics/claude-code) 的完整源代码。然而，泄露的内容仅包含 `src/` 目录——没有构建配置、没有依赖清单、没有核心模块的类型定义，无法直接编译或运行。

**本项目做了什么？** 我们补全了所有缺失的部分：

- 📦 `package.json` 与依赖声明
- ⚙️ `tsconfig.json` 与构建脚本
- 🧩 185+ 个存根/类型文件
- 🔧 内部私有包的兼容 shim
- 🚀 `bun:bundle` 特性标志运行时

最终结果是一个**完整可构建、可在本地运行**的 Claude Code 终端应用。

---

## ✨ 核心特性

| 功能 | 状态 |
|------|------|
| 🖥️ 交互式 REPL | ✅ 完整可用 |
| 🔑 Anthropic API 集成 | ✅ 完整可用 |
| 🛠️ 工具系统（Bash、Edit、Read 等） | ✅ 完整可用 |
| 🔐 OAuth 登录 & API Key 认证 | ✅ 完整可用 |
| 🤝 MCP 服务器集成 | ✅ 完整可用 |
| 🎨 Ink 终端 UI（React 驱动） | ✅ 完整可用 |
| 🎤 语音模式 / 桥接守护进程等 | ❌ 已通过特性标志禁用 |

---

## 🚀 快速开始

### 1. 安装 Bun

```bash
curl -fsSL https://bun.sh/install | bash
```

### 2. 克隆并安装依赖

```bash
git clone https://github.com/weikma/claude-code-rebuilt.git
cd claude-code-rebuilt
bun install
```

### 3. 配置 API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 4. 启动！

```bash
bun run start
```

你将看到与官方版本几乎完全一致的 Claude Code 终端界面。🎉

---

## 🔗 项目地址

**GitHub:** [https://github.com/weikma/claude-code-rebuilt](https://github.com/weikma/claude-code-rebuilt)

欢迎 ⭐ Star、提 Issue 或参与讨论！

---

## 🛠️ 技术栈

- **语言：** TypeScript（strict 模式，512K+ 行）
- **运行时：** [Bun](https://bun.sh)
- **终端 UI：** [React](https://react.dev) + [Ink](https://github.com/vadimdemedes/ink)
- **CLI 解析：** [Commander.js](https://github.com/tj/commander.js)
- **Schema 校验：** [Zod](https://zod.dev)
- **API：** [Anthropic SDK](https://docs.anthropic.com)

