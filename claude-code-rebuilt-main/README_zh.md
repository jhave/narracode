<div align="center">

# Claude Code Rebuilt

**完全复原可用的 Anthropic Claude Code CLI**

English | [中文](./README_zh.md)

[![TypeScript](https://img.shields.io/badge/TypeScript-512K%2B_lines-3178C6?logo=typescript&logoColor=white)](#技术栈)
[![Bun](https://img.shields.io/badge/Runtime-Bun-f472b6?logo=bun&logoColor=white)](#技术栈)
[![React + Ink](https://img.shields.io/badge/UI-React_%2B_Ink-61DAFB?logo=react&logoColor=black)](#技术栈)
[![Files](https://img.shields.io/badge/~1,900_files-source_only-grey)](#项目结构)

</div>

---

## 目录

- [Claude Code Rebuilt](#claude-code-rebuilt)
  - [目录](#目录)
  - [背景](#背景)
  - [技术栈](#技术栈)
  - [快速开始](#快速开始)
    - [1. 安装 Bun](#1-安装-bun)
    - [2. 安装依赖](#2-安装依赖)
    - [3. 设置 API 密钥](#3-设置-api-密钥)
    - [4. 启动应用](#4-启动应用)
  - [使用方法](#使用方法)
  - [构建](#构建)
  - [项目结构](#项目结构)
  - [工作原理](#工作原理)
  - [已解锁的斜杠命令](#已解锁的斜杠命令)
  - [备注](#备注)
  - [免责声明](#免责声明)

---

## 背景

2026 年 3 月 31 日，Anthropic 的 Claude Code 完整源码通过其 npm 注册表中暴露的 source map 文件泄露。[泄露的源码](https://github.com/instructkr/claw-code) 仅包含 `src/` 目录——没有构建配置、没有依赖清单、没有核心模块的类型定义，也无法编译或运行。

本项目重建了所有缺失的部分：`package.json`、`tsconfig.json`、构建脚本、185+ 个 stub/类型文件、内部专用包的兼容 shim，以及 `bun:bundle` 特性标记运行时。最终产出是一个完整的、可构建的、可运行的 Claude Code 终端应用程序。仅限 Anthropic 内部的功能（daemon workers、语音模式、computer-use 等）在构建时通过特性标记禁用；核心的交互式 REPL、工具系统和 Anthropic API 集成保持完全可用。

---

## 技术栈

| 类别 | 技术 |
|---|---|
| 语言 | [TypeScript](https://www.typescriptlang.org/)（严格模式） |
| 运行时 | [Bun](https://bun.sh) |
| 终端 UI | [React](https://react.dev) + [Ink](https://github.com/vadimdemedes/ink) |
| CLI 解析 | [Commander.js](https://github.com/tj/commander.js)（extra-typings） |
| Schema 验证 | [Zod](https://zod.dev) |
| 协议 | [MCP SDK](https://modelcontextprotocol.io) · LSP |
| API | [Anthropic SDK](https://docs.anthropic.com) |
| 认证 | OAuth 2.0 · API Key · macOS Keychain |

---

## 快速开始

### 1. 安装 Bun

Claude Code 运行在 [Bun](https://bun.sh/)（v1.1+）上。如果尚未安装：

```bash
curl -fsSL https://bun.sh/install | bash
```

### 2. 安装依赖

```bash
bun install
```

### 3. 设置 API 密钥

你需要一个 [Anthropic API 密钥](https://console.anthropic.com/)，或者可以使用 OAuth 登录（在 REPL 中输入 `/login`）：

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 4. 启动应用

```bash
# 启动交互式 REPL
bun run start
```

完成——你应该能看到 Claude Code 的终端 UI。

---

## 使用方法

```bash
# 打印版本
bun run start -- --version

# 显示所有 CLI 参数和子命令
bun run start -- --help

# 单次提问（支持管道，输出响应后退出）
bun run start -- --print "explain this codebase"

# 最小化启动（跳过 hooks、插件、自动记忆）
bun run start -- --bare

# 传入系统提示词
bun run start -- --system-prompt "You are a Go expert"

# 使用指定模型
bun run start -- --model sonnet
```

---

## 构建

生成单文件 bundle：

```bash
# 构建到 dist/cli.js
bun run build

# 运行构建产物
bun dist/cli.js
bun dist/cli.js --help
```

---

## 项目结构

```
.
├── src/
│   ├── entrypoints/cli.tsx   # 进程入口
│   ├── main.tsx              # Commander CLI 配置、REPL 启动
│   ├── commands.ts           # 斜杠命令注册
│   ├── tools.ts              # 工具注册（Bash、Edit、Read 等）
│   ├── Tool.ts               # 基础工具类型定义
│   ├── query.ts              # LLM 查询引擎
│   ├── ink/                  # 内置 Ink 终端渲染器
│   ├── components/           # React 终端 UI 组件
│   ├── screens/              # 全屏 UI（REPL、Doctor、Resume）
│   ├── services/             # API 客户端、MCP、分析、压缩
│   ├── hooks/                # React hooks
│   ├── utils/                # 工具函数
│   ├── types/                # 重建的类型定义
│   └── _external/            # 构建兼容层
│       ├── preload.ts        # 运行时 MACRO + bun:bundle shim
│       ├── globals.d.ts      # MACRO 类型声明
│       └── shims/            # 私有依赖的 stub 包
├── scripts/
│   └── build-external.ts     # Bun.build() 带特性标记 + 定义
├── package.json
├── tsconfig.json
└── bunfig.toml               # Preload 配置 + .md 文本加载器
```

---

## 工作原理

原版 Claude Code 源码依赖 Bun 的 `bun:bundle` 模块实现编译时特性标记，以及 `MACRO.*` 全局变量实现构建时常量。本项目提供了：

1. **`bunfig.toml` + `preload.ts`** —— 注册 Bun 插件，在运行时解析 `import { feature } from 'bun:bundle'`，并将 `MACRO.VERSION` 等定义为全局变量。
2. **`scripts/build-external.ts`** —— 一个 `Bun.build()` 脚本，通过插件替换 `bun:bundle`，通过 `define` 注入 `MACRO.*`，并将私有包标记为 external。所有 90+ 个内部特性标记均被禁用；仅启用少数安全标记。
3. **`src/_external/shims/` 下的 stub 包** —— 为不可公开获取的 `@ant/*` 内部包和原生 NAPI 插件提供轻量级空操作模块。
4. **重建的类型文件** —— `src/types/message.ts`、`src/types/tools.ts` 及其他高扇出模块，这些在泄露源码中缺失。

---

## 已解锁的斜杠命令

原版 Claude Code 中有许多斜杠命令被内部特性标记（Feature Flag）隐藏，在外部构建中默认禁用。本项目已重建并完全解锁以下命令，无需任何 Flag 服务即可在本地使用：

| 命令 | 描述 | 原始 Flag |
| ------- | ----------- | ------------- |
| `/brief` | 切换简洁输出模式——可见输出仅通过 `SendUserMessage` 工具发送 | `KAIROS` / `KAIROS_BRIEF` |
| `/buddy` | 召唤虚拟同伴，特征由种子 PRNG 确定性生成 | `BUDDY` |
| `/fork` | 生成后台子智能体，继承完整的对话上下文 | `FORK_SUBAGENT` |

关于全部 14 个被特性标记控制的命令的详细分析（包括哪些已完整实现、部分 stub、或完全缺失），请参阅 [FEATURE_FLAG_COMMANDS_ANALYSIS.md](./FEATURE_FLAG_COMMANDS_ANALYSIS.md)。

---

## 备注

- 除上述已解锁的命令外，其他被禁用特性标记保护的功能（语音、bridge、daemon、coordinator、assistant/Kairos 等）仍不可用。
- 交互式 REPL、`--print` 模式、`--help` 以及完整的 Commander 选项均可正常工作。
- 认证（API 密钥和 OAuth）、Anthropic API 调用、工具执行、MCP 服务器集成以及基于 Ink 的终端 UI 均从原始源码中保留。

---

## 免责声明

**所有原始 Claude Code 源码均为 [Anthropic, PBC](https://www.anthropic.com/) 的知识产权。** 本仓库基于无意间暴露的源码，仅**严格用于研究、教育和存档目的**。

- 本项目**不附带任何许可证**。不授予任何用于商业目的的使用、修改、分发或创建衍生作品的权限。
- 这是一个独立的重建工作，**与 Anthropic 没有任何关联、背书或赞助关系**。
- 如果您是 Anthropic 的代表并希望移除此仓库，请提交 issue 或直接联系维护者 ([@weikma](https://github.com/weikma))。
