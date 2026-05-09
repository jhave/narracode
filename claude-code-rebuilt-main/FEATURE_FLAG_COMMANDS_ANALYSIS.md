# Feature Flag 控制命令分析报告

> 分析日期: 2026-04-02
> 代码库: claude-code-rebuilt (从泄露源码重建)

## 概览

本项目共有 **14 个** Feature Flag 控制的斜杠命令，均在外部构建中通过 `scripts/build-external.ts` 的 `EXTERNAL_DISABLED_FEATURES` 列表禁用。Feature Flag 系统通过 `src/_external/bun-bundle.ts` 中的 `feature()` 函数实现编译期死代码消除。

### 状态总览

| 命令 | Feature Flag | 实现状态 | 能否补全 |
|------|-------------|---------|---------|
| `/proactive` | `PROACTIVE` / `KAIROS` | **缺失** | 困难 |
| `/brief` | `KAIROS` / `KAIROS_BRIEF` | **完整** | 已完整 |
| `/remote-control` | `BRIDGE_MODE` | **完整** | 已完整 |
| `/remote-control-server` | `DAEMON` + `BRIDGE_MODE` | **缺失** | 中等 |
| `/voice` | `VOICE_MODE` | **完整** | 已完整 |
| `/force-snip` | `HISTORY_SNIP` | **缺失** | 困难 |
| `/workflows` | `WORKFLOW_SCRIPTS` | **缺失** | 困难 |
| `/web` | `CCR_REMOTE_SETUP` | **完整** | 已完整 |
| `/torch` | `TORCH` | **缺失** | 不可行 |
| `/peers` | `UDS_INBOX` | **缺失** | 困难 |
| `/fork` | `FORK_SUBAGENT` | **缺失** | 简单 |
| `/buddy` | `BUDDY` | **缺失** | 中等 |
| `/subscribe-pr` | `KAIROS_GITHUB_WEBHOOKS` | **缺失** | 困难 |
| `/ultraplan` | `ULTRAPLAN` | **完整** | 已完整 |

- **完整**: 5 个 — 开启 Feature Flag 即可使用
- **缺失**: 9 个 — 需要不同程度的补全工作

---

## 已完整实现的命令 (5 个)

### 1. `/brief` — 简洁输出模式

**Feature Flag**: `KAIROS` 或 `KAIROS_BRIEF`
**文件**: `src/commands/brief.ts` (131 行)
**类型**: `local`

**功能描述**:
切换 Brief-Only 模式（聊天模式）。启用后，用户可见的输出仅通过 `SendUserMessage` 工具发送，其余文本仅在详情视图中显示。设计用于更简洁的对话体验。

**核心机制**:
- 双向状态同步: 通过 `setUserMsgOptIn()` 与 `context.setAppState()` 管理
- 权限检查: GrowthBook 远程开关 `tengu_kairos_brief` (5 分钟 TTL) 作为 kill-switch
- 环境变量旁路: `CLAUDE_CODE_BRIEF=true` 用于开发测试
- 关闭操作不受权限限制 (防止用户被锁定)

**依赖完整性**: 全部存在且完整 — `BriefTool`, `state.ts`, `growthbook.ts`, `analytics`

**启用方式**: 在 `scripts/build-external.ts` 的 `ENABLED_FEATURES` 中添加 `KAIROS_BRIEF`

---

### 2. `/remote-control` — 远程控制桥接

**Feature Flag**: `BRIDGE_MODE`
**文件**: `src/commands/bridge/index.ts`, `src/commands/bridge/bridge.tsx`
**类型**: `local-jsx`
**别名**: `/rc`

**功能描述**:
建立本地 CLI 与 claude.ai 之间的双向桥接连接。支持远程控制会话，用户可在 Web 端操作本地 Claude Code 实例。

**核心机制**:
- 会话注册: 向桥接服务器注册本地环境
- 工作轮询: 持续轮询来自 claude.ai 的工作请求
- WebSocket 传输: 支持 v1 (环境绑定) 和 v2 (无环境) 两种协议
- QR 码支持: 移动端快捷访问
- 权限路由: 通过 `BridgePermissionCallbacks` 处理远程权限请求

**依赖完整性**: `src/bridge/` 目录下 31 个文件全部存在且实现完整，`AppState` 集成 12+ 个桥接状态字段

**前置条件**: OAuth 认证 + 组织策略 `allow_remote_control` + GrowthBook 开关 `tengu_ccr_bridge`

**启用方式**: 在 `ENABLED_FEATURES` 中添加 `BRIDGE_MODE`

---

### 3. `/voice` — 语音输入模式

**Feature Flag**: `VOICE_MODE`
**文件**: `src/commands/voice/index.ts`, `src/commands/voice/voice.ts` (5,264 字节)
**类型**: `local`

**功能描述**:
切换按住说话语音输入。使用 Anthropic 的 `voice_stream` 端点进行语音转文字 (STT)。

**核心机制**:
- 麦克风权限检查: `requestMicrophonePermission()` (macOS/Linux)
- 三种录音后端: 原生音频模块 (`audio-capture-napi`)、`arecord` (ALSA)、SoX
- WebSocket STT: 通过 OAuth 令牌连接 `voice_stream` API
- 语言支持: 20+ 种语言的归一化处理
- GrowthBook kill-switch: `tengu_cobalt_frost` 控制 Nova 3 STT 引擎选择

**依赖完整性**: 全部存在 — `voiceStreamSTT.ts` (WebSocket 客户端)、`voice.ts` (录音服务)、`useVoice.ts` (React Hook)

**限制**: 仅 claude.ai 订阅用户可用 (`availability: ['claude-ai']`)

**启用方式**: 在 `ENABLED_FEATURES` 中添加 `VOICE_MODE`

---

### 4. `/web` — Web 远程环境设置

**Feature Flag**: `CCR_REMOTE_SETUP`
**文件**: `src/commands/remote-setup/index.ts`, `remote-setup.tsx`, `api.ts` (共 388 行)
**类型**: `local-jsx`

**功能描述**:
设置 Claude Code 的 Web 环境 (CCR - Claude Code Remote)，将本地 GitHub 认证导入到云端。

**核心流程**:
1. 检查 claude.ai 登录状态
2. 检查 GitHub CLI (`gh`) 安装和认证状态
3. 获取 GitHub Token 并通过 HTTP POST 导入到 CCR 后端 (Fernet 加密存储)
4. 尽力创建默认 Anthropic Cloud 环境 (Python 3.11 + Node.js 20)
5. 打开浏览器到 `claude.ai/code`

**依赖完整性**: 11+ 直接依赖全部存在且功能完整，包括 teleport API、GitHub 工具、UI 组件

**启用方式**: 在 `ENABLED_FEATURES` 中添加 `CCR_REMOTE_SETUP`

---

### 5. `/ultraplan` — 多智能体远程规划

**Feature Flag**: `ULTRAPLAN`
**文件**: `src/commands/ultraplan.tsx` (66,629 字节)
**类型**: `local-jsx`

**功能描述**:
启动运行在 CCR 上的多智能体规划会话。利用最强模型 (Opus 4.6) 生成高级计划，用户可编辑、批准后在远程执行或传送回本地终端。设计用于需要 10-30 分钟扩展推理的复杂任务。

**核心机制**:
- 远程会话创建: 通过 `teleportToRemote()` 在 CCR 上启动计划模式
- 轮询循环: `pollForApprovedExitPlanMode()` 监控计划完成状态
- 双执行路径: 远程执行 (用户在浏览器批准) 或 传送回本地
- 任务生命周期: 通过 `RemoteAgentTask` 框架管理
- 分析集成: 完整的事件日志

**依赖完整性**: 18+ 直接依赖全部验证存在

**已知限制**:
- OAuth 令牌刷新存在 30 分钟超时问题 (代码中有 TODO 注释)
- `src/utils/ultraplan/prompt.txt` 为 0 字节 (提示词模板内容为空)
- `isEnabled` 硬编码为 `"external" === 'ant'`，外部构建中永远为 false

**启用方式**: 在 `ENABLED_FEATURES` 中添加 `ULTRAPLAN`，并需要修改 `isEnabled` 条件

---

## 缺失但可补全的命令 (4 个)

### 6. `/fork` — 分叉子智能体

**Feature Flag**: `FORK_SUBAGENT`
**预期文件**: `src/commands/fork/index.js` (缺失)
**补全难度**: **简单**

**功能描述**:
启用后台工作进程，继承父级的完整对话上下文和系统提示。当 Agent 工具调用中省略 `subagent_type` 时，隐式创建分叉。分叉智能体独立处理指令，设计为缓存一致 (cache-identical) 的 API 请求以最大化 prompt cache 命中率。

**基础设施状态** (95% 完整):

| 组件 | 文件 | 状态 |
|------|------|------|
| 分叉子智能体核心 | `src/tools/AgentTool/forkSubagent.ts` (211 行) | 完整 |
| 分叉执行器 | `src/utils/forkedAgent.ts` (690 行) | 完整 |
| 防递归守卫 | `src/constants/xml.ts` (`FORK_BOILERPLATE_TAG`) | 完整 |
| 分支别名兼容 | `src/commands/branch/index.ts:8` | 完整 |
| 斜杠命令处理 | `src/utils/processUserInput/processSlashCommand.tsx` | 完整 |

**缺失**: 仅 `src/commands/fork/index.js` 命令入口文件

**补全方案**: 创建简单的命令包装器，调用已有的 `forkSubagent.ts` 基础设施。当功能禁用时，`/branch` 命令会自动提供 `fork` 别名作为降级方案。

---

### 7. `/buddy` — 虚拟同伴角色

**Feature Flag**: `BUDDY`
**预期文件**: `src/commands/buddy/index.js` (缺失)
**补全难度**: **中等**

**功能描述**:
提供虚拟 AI 同伴角色，使用种子 PRNG (Mulberry32) 确定性生成唯一同伴，具有物种、稀有度、属性和个性等特征。

**已有基础设施**:

| 组件 | 文件 | 状态 |
|------|------|------|
| 类型定义 | `src/buddy/types.ts` | 完整 |
| 同伴生成逻辑 | `src/buddy/companion.ts` | 完整 |
| 精灵渲染组件 | `src/buddy/CompanionSprite.tsx` (45KB) | 完整 |
| 精灵动画 | `src/buddy/sprites.ts` | 完整 |
| 通知 Hook | `src/buddy/useBuddyNotification.tsx` | 完整 |
| 交互提示词 | `src/buddy/prompt.ts` | 完整 |

**缺失**: 命令入口文件 + 同伴状态持久化/配置管理逻辑

**补全方案**: 创建 `local-jsx` 类型的命令，整合已有的 companion 生成和 UI 渲染组件。需要设计状态存储方案 (配置文件中保存 companion seed)。

---

### 8. `/remote-control-server` — 远程控制守护进程

**Feature Flag**: `DAEMON` + `BRIDGE_MODE`
**预期文件**: `src/commands/remoteControlServer/index.js` (缺失)
**补全难度**: **中等**

**功能描述**:
启动持久运行的守护进程，注册长期桥接环境，持续轮询工作请求，为每个传入的工作项生成子会话。

**会话生成模式** (来自 `bridge/types.ts:SpawnMode`):
- `single-session`: 单会话模式，会话结束后桥接拆除
- `worktree`: 持久服务器，每个会话获得隔离的 git worktree
- `same-dir`: 持久服务器，会话共享工作目录

**已有基础设施**:
- `src/bridge/` 下 31 个桥接文件全部完整
- `src/bridge/remoteBridgeCore.ts` — 非 REPL 桥接包装器 (部分实现)
- `src/bridge/sessionRunner.ts` — 会话执行包装器
- `AppState` 桥接集成

**缺失**:
- 命令入口文件
- `src/daemon/main.ts` 为空 stub: `export async function daemonMain(_args: string[]): Promise<void> {}`
- 进程生成与生命周期管理
- 守护进程 IPC 通信机制

**补全方案**: 需要实现守护进程启动/关闭管理、进程生成策略 (worktree/same-dir)、健康检查与错误恢复。可复用完整的桥接基础设施。

---

### 9. `/ultraplan` 的提示词补全

虽然 `/ultraplan` 命令本身已完整实现，但 `src/utils/ultraplan/prompt.txt` 为 0 字节。如需完整功能，需要补充计划模式系统指令的提示词内容。

---

## 缺失且难以补全的命令 (5 个)

### 10. `/proactive` — 主动自治模式

**Feature Flag**: `PROACTIVE` 或 `KAIROS`
**预期文件**: `src/commands/proactive.js` (缺失)
**补全难度**: **困难**

**功能描述**:
切换主动/自治模式。模型无需等待用户输入即可主动探索、行动。系统通过周期性 `<tick>` 提示实现定期检查，模型可调用 `Sleep` 工具进行等待。

**系统提示中的描述**: *"You are in proactive mode. Take initiative — explore, act, and make progress without waiting for instructions."* (main.tsx:2203)

**已有集成点**:
- `main.tsx` (行 1864, 2197-2203): 系统提示和 tick 机制设置
- `REPL.tsx` (行 194, 687, 2116, 2606-2638 等): UI 响应性
- `tools.ts` (行 25-28): 条件加载 `SleepTool`
- `compact/prompt.ts`: 恢复 proactive 会话的特殊提示

**缺失组件**:

| 组件 | 状态 | 说明 |
|------|------|------|
| 命令文件 `proactive.js` | **缺失** | 切换入口 |
| `SleepTool` | **缺失** | `src/tools/SleepTool/SleepTool.js` 不存在 |
| Proactive 模块 | **Stub** | `src/proactive/index.ts` 所有函数均为 no-op |
| Tick 调度基础设施 | **缺失** | 无周期性唤醒机制 |

**补全障碍**: 需要实现完整的 tick 调度引擎、SleepTool、状态管理，以及理解 Kairos 生态系统的设计意图。代码库中虽有大量集成点，但核心逻辑完全缺失。

---

### 11. `/force-snip` — 强制历史裁剪

**Feature Flag**: `HISTORY_SNIP`
**预期文件**: `src/commands/force-snip.js` (缺失)
**补全难度**: **困难**
**限制**: ANT-ONLY (内部构建专用)

**功能描述**:
手动触发历史裁剪 (snipping)，将对话历史折叠为压缩的边界标记，释放上下文窗口空间。

**已有集成点**:
- `query.ts` (行 115-116, 396-409): 条件加载 snip 模块、`snipCompactIfNeeded()` 调用
- `tools.ts`: 条件加载 `SnipTool`

**缺失组件**:

| 组件 | 状态 |
|------|------|
| 命令文件 `force-snip.js` | **缺失** |
| `SnipTool` (`src/tools/SnipTool/SnipTool.js`) | **缺失** |
| `snipCompact.ts` | **Stub** (返回 `{ messages, tokensFreed: 0 }`) |
| `snipProjection.ts` | **Stub** (返回未过滤消息) |

**补全障碍**: 需要设计消息裁剪算法、边界标记消息类型、token 计数与预算管理。这是一个独立的消息压缩子系统，算法复杂度较高。

---

### 12. `/workflows` — 工作流脚本

**Feature Flag**: `WORKFLOW_SCRIPTS`
**预期文件**: `src/commands/workflows/index.js` (缺失)
**补全难度**: **困难**

**功能描述**:
管理和执行工作流脚本，从工作流定义动态创建命令。

**已有基础设施** (仅 Stub):

| 组件 | 文件 | 状态 |
|------|------|------|
| 工具常量 | `src/tools/WorkflowTool/constants.ts` | 仅 `WORKFLOW_TOOL_NAME = 'Workflow'` |
| 类型定义 | `src/tools/WorkflowTool/types.ts` | 最小 Stub (212 字节) |
| 工具实现 | `src/tools/WorkflowTool/WorkflowTool.ts` | 空 Stub (915 字节) |
| 命令工厂 | `src/tools/WorkflowTool/createWorkflowCommand.js` | **缺失** |
| 命令入口 | `src/commands/workflows/index.js` | **缺失** |

**集成引用**:
- `commands.ts` (行 401-405): 动态调用 `getWorkflowCommands(cwd)` 发现工作流命令
- `commands.ts` (行 457): 运行时工作流命令注入

**补全障碍**: 需要设计完整的工作流定义格式、解析器、发现机制和执行引擎。几乎零实现基础。

---

### 13. `/peers` — 对等实例发现

**Feature Flag**: `UDS_INBOX`
**预期文件**: `src/commands/peers/index.js` (缺失)
**补全难度**: **困难**

**功能描述**:
发现和管理同一机器上运行的其他 Claude Code 实例 (通过 Unix Domain Socket) 或远程实例 (通过 Bridge 会话)。用户可通过 `SendMessage` 工具向 peer 发送消息 (`uds:/path/to.sock` 或 `bridge:session_id`)。

**缺失组件**:

| 组件 | 状态 |
|------|------|
| 命令入口 `peers/index.js` | **缺失** |
| `ListPeersTool` (`src/tools/ListPeersTool/ListPeersTool.js`) | **缺失** |
| UDS 消息系统 (`src/utils/udsMessaging.ts`) | **全 Stub** |

UDS 消息系统所有函数均为空实现:
- `getDefaultUdsSocketPath()` → 返回空字符串
- `getUdsMessagingSocketPath()` → 返回 undefined
- `startUdsMessaging()` → no-op

**已有相关组件**:
- `SendMessageTool` (`src/tools/SendMessageTool/`) — 存在且支持 `uds:` 和 `bridge:` URI
- `main.tsx` (行 1910-1912): 接受 `--messaging-socket-path` 选项
- `setup.ts` (行 95-98): 启动时初始化 UDS 消息服务器

**补全障碍**: 需要实现完整的 Unix Domain Socket 服务器、peer 发现协议、ListPeersTool。这是底层 IPC 基础设施工作。

---

### 14. `/subscribe-pr` — GitHub Webhook 订阅

**Feature Flag**: `KAIROS_GITHUB_WEBHOOKS`
**预期文件**: `src/commands/subscribe-pr.js` (缺失)
**补全难度**: **困难**

**功能描述**:
启用 GitHub webhook 集成，自动将 GitHub 事件注入 Claude Code 会话，用于持续代码审查和监控。

**缺失组件**:

| 组件 | 状态 |
|------|------|
| 命令文件 `subscribe-pr.js` | **缺失** |
| `SubscribePRTool` (`src/tools/SubscribePRTool/SubscribePRTool.js`) | **缺失** |

**已有支持代码**:
- `UserTextMessage.tsx`: 检查 `KAIROS_GITHUB_WEBHOOKS` 并渲染 `<github-webhook-activity>` XML
- `useReplBridge.tsx`: 通过 `sanitizeInboundWebhookContent` 清理传入 webhook 内容

**补全障碍**: 需要 GitHub Webhook 注册/管理 API、事件解析路由、以及与桥接系统的集成。涉及外部服务交互，复杂度高。

---

### 15. `/torch` — 用途不明

**Feature Flag**: `TORCH`
**预期文件**: `src/commands/torch.js` (缺失)
**补全难度**: **不可行**

**状态**: 代码库中除 Feature Flag 声明和 `commands.ts` 的条件导入外，无任何相关实现或引用。无法推断其设计意图，无法补全。

---

## Feature Flag 系统说明

### 机制

```
src/_external/bun-bundle.ts  →  声明 FEATURE_MAP (90个 flag)
                                  ↓
scripts/build-external.ts    →  构建时替换 feature() 为硬编码列表
                                  ↓
src/commands.ts              →  条件 require() 实现死代码消除
```

### 当前构建配置

**默认启用** (仅 3 个):
- `AUTO_THEME` — 自动主题
- `BREAK_CACHE_COMMAND` — 缓存清除命令
- `BUILTIN_EXPLORE_PLAN_AGENTS` — 内建探索/规划 Agent

**全部 14 个命令相关 Flag 均在 `EXTERNAL_DISABLED_FEATURES` 列表中**, 需手动移至 `ENABLED_FEATURES` 才能激活。

### 启用指南

修改 `scripts/build-external.ts`:

```typescript
// 将目标 flag 从 EXTERNAL_DISABLED_FEATURES 移至此处
const ENABLED_FEATURES = new Set([
  "AUTO_THEME",
  "BREAK_CACHE_COMMAND",
  "BUILTIN_EXPLORE_PLAN_AGENTS",
  // 添加想要启用的 flag:
  // "VOICE_MODE",
  // "FORK_SUBAGENT",
  // ...
]);
```

---

## 补全优先级建议

| 优先级 | 命令 | 理由 |
|--------|------|------|
| P0 | `/brief` `/voice` `/remote-control` `/web` `/ultraplan` | 已完整，仅需开启 Flag |
| P1 | `/fork` | 仅缺命令入口，基础设施 95% 就绪 |
| P2 | `/buddy` | UI 组件完整，缺命令包装和状态管理 |
| P2 | `/remote-control-server` | 桥接基础设施完整，需实现守护进程逻辑 |
| P3 | `/proactive` | 集成点丰富但核心逻辑全是 Stub |
| P3 | `/force-snip` | 需设计消息裁剪算法 |
| P3 | `/peers` | 需实现底层 UDS IPC |
| P3 | `/subscribe-pr` | 需外部服务集成 |
| P4 | `/workflows` | 几乎零实现基础 |
| P4 | `/torch` | 无法推断意图 |
