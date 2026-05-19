# 今日老婆 JRLP

<p align="center">
  <img src="https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat&logo=typescript&logoColor=white">
  <img src="https://img.shields.io/badge/SealDice-Plugin-2ecc71?style=flat&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg?style=flat&logo=apache&logoColor=white">
</p>

海豹骰 (SealDice) 今日老婆插件 — 每日随机 GalGame / Anime 角色，支持结婚系统与自定义文案模板。

## 功能

- **今日老婆** (`.jrlp`) — 每日随机获取一位角色作为今日老婆
- **换老婆** (`.hlp`) — 不满意可以换，每日有次数限制（默认 5 次）
- **结婚** (`.jrlp 结婚`) — 与当前老婆结婚，婚姻期间固定显示该角色
- **离婚** (`.jrlp 离婚`) — 手动解除婚姻关系
- **状态查询** (`.jrlp status`) — 查看后端服务状态
- **婚姻到期自动解除** — 每日定时任务检查 + 惰性检查双重保障
- **全文案模板可配置** — 所有回复文案均支持多条随机 + 占位符替换

## 快速开始

### 后端部署

```bash
cd backend
uv sync
uv run python main.py
```

可选参数：

- `--host 0.0.0.0` — 绑定地址（默认 `0.0.0.0`）
- `--port 18428` — 绑定端口（默认 `18428`）
- `--debug` — 开启调试模式（启用热重载 + 调试日志）

将角色图片放入 `backend/img/` 目录（支持子目录），文件名即角色名（不含扩展名）。

### 插件安装

1. 从 [Releases](https://github.com/shifeifenming/jrlp/releases) 下载 `jrlp.js`
2. 在海豹骰管理面板 → 插件管理 → 上传安装
3. 在插件配置中设置 `api_url` 为你的后端地址

或从源码构建：

```bash
pnpm install
pnpm run build
# 产物在 dist/jrlp.js
```

## 命令

| 命令           | 说明                         |
| -------------- | ---------------------------- |
| `.jrlp`        | 获取/显示今日老婆            |
| `.hlp`         | 换一位老婆（有每日次数限制） |
| `.jrlp 结婚`   | 与今日老婆结婚               |
| `.jrlp 离婚`   | 解除婚姻关系                 |
| `.jrlp status` | 查看后端服务状态             |

## 配置项

在海豹骰插件配置面板中可调整：

| 配置                | 类型   | 默认值                   | 说明                         |
| ------------------- | ------ | ------------------------ | ---------------------------- |
| `debug`             | bool   | `false`                  | 调试模式（报告问题前请启用） |
| `useSealCode`       | bool   | `false`                  | 使用海豹码代替 CQ 码         |
| `useBase64CQ`       | bool   | `false`                  | 使用 base64 CQ Code          |
| `noFormat`          | bool   | `false`                  | 不执行 seal.format           |
| `api_url`           | string | `http://localhost:18428` | 后端 API 地址                |
| `daily_hlp_limit`   | int    | `5`                      | 每天换老婆次数上限           |
| `retry_times`       | int    | `3`                      | API 失败重试次数             |
| `retry_interval`    | int    | `1000`                   | 重试间隔 (ms)                |
| `marriage_duration` | int    | `7`                      | 结婚维持天数                 |

## 文案模板

所有文案均支持**多条随机抽取**，在海豹骰配置面板中以数组形式配置。

### 可用占位符

| 占位符         | 说明                                                 |
| -------------- | ---------------------------------------------------- |
| `{{老婆图片}}` | 角色图片（自动根据配置选择 CQ/SealCode/Base64 格式） |
| `{{老婆名字}}` | 角色名称                                             |
| `{{玩家}}`     | 当前玩家（转义为豹语 `{$t玩家}`）                    |
| `{{天数}}`     | 已婚天数                                             |
| `{{剩余天数}}` | 婚姻剩余天数                                         |
| `{{次数上限}}` | 每日换老婆次数上限                                   |
| `{{用户头像}}` | 用户 QQ 头像（⚠️ 仅 QQ 平台可用）                    |

模板处理流程：随机抽取一条 → 替换 `{{xxx}}` 占位符 → `seal.format()` 处理豹语表达式 → 发送

### 模板列表

| 配置键               | 用途           | 默认文案                                                                               |
| -------------------- | -------------- | -------------------------------------------------------------------------------------- |
| `tpl_jrlp`           | 今日老婆       | `{{老婆图片}}\n{{玩家}}今天的老婆是{{老婆名字}}`                                       |
| `tpl_hlp`            | 换老婆成功     | `{{老婆图片}}\n{{玩家}}的新老婆是{{老婆名字}}`                                         |
| `tpl_hlp_limit`      | 换老婆达到上限 | `{{老婆图片}}\n{{玩家}}今天的老婆是{{老婆名字}}\n(每天最多换{{次数上限}}次老婆哦)`     |
| `tpl_marry`          | 结婚           | `{{老婆图片}}\n恭喜{{玩家}}与{{老婆名字}}喜结连理！`                                   |
| `tpl_married_status` | 已婚状态       | `{{老婆图片}}\n{{玩家}}与{{老婆名字}}已经幸福地生活了{{天数}}天\n(剩余{{剩余天数}}天)` |
| `tpl_divorce`        | 离婚           | `{{玩家}}与{{老婆名字}}的缘分走到了尽头...`                                            |
| `tpl_not_married`    | 未婚时离婚     | `你还没有结婚哦`                                                                       |
| `tpl_no_wife_marry`  | 无老婆时结婚   | `你还没有今日老婆，先用 .jrlp 获取一位吧`                                              |
| `tpl_hlp_blocked`    | 婚姻期间换老婆 | `你已经结婚了，不能换老婆哦！\n如需解除关系请使用 .jrlp 离婚`                          |

## 项目结构

```
├── src/                  # TypeScript 插件源码
│   ├── index.ts          # 入口：注册扩展、配置、命令、定时任务
│   ├── config.ts         # 配置注册与读取
│   ├── api.ts            # HTTP API 调用（带重试）
│   ├── commands.ts       # 命令处理逻辑
│   ├── formatter.ts      # 文案格式化
│   ├── template.ts       # 模板引擎（随机 + 占位符 + seal.format）
│   ├── state.ts          # 每日状态管理（老婆缓存、换老婆计数）
│   ├── storage.ts        # 全局数据持久化（ext.storageSet/Get）
│   ├── marriage.ts       # 结婚/离婚/过期逻辑
│   └── logger.ts         # 调试日志
├── backend/              # FastAPI 后端（uv 管理）
│   ├── main.py           # 服务入口
│   ├── pyproject.toml    # Python 项目配置与依赖
│   ├── uv.lock           # 依赖锁定文件
│   ├── imageDownloader.py # 批量图片下载工具
│   ├── rename.py         # 文件名批量重命名工具
│   └── img/              # 角色图片目录
├── tools/                # 构建工具
│   ├── build.js          # esbuild 打包脚本
│   └── build-config.js   # 构建配置
├── types/                # TypeScript 类型定义
│   └── seal.d.ts         # SealDice JS SDK 类型
├── dist/                 # 构建产物（.gitignore）
├── biome.json            # Biome 代码检查配置
├── tsconfig.json         # TypeScript 配置
└── package.json          # 插件项目配置（pnpm）
```

## 开发

```bash
# 安装依赖
pnpm install

# 开发构建（含 sourcemap）
pnpm run dev

# 生产构建
pnpm run build

# 类型检查
pnpm run typecheck

# 代码检查
pnpm run check

# 格式化
pnpm run format
```

## 后端 API

| 端点                       | 方法 | 参数                           | 说明                                                    |
| -------------------------- | ---- | ------------------------------ | ------------------------------------------------------- |
| `/api/v1/character/random` | GET  | `?image_format=base64`（可选） | 返回随机角色 `{ filename, image_sub [, image_base64] }` |
| `/api/v1/status`           | GET  | —                              | 服务状态（CPU、内存、图片数、访问统计）                 |
| `/img/{path}`              | GET  | —                              | 静态图片访问                                            |

## 致谢

- [海豹骰 SealDice](https://github.com/sealdice) — 骰子机器人框架
- [sealdice-js-ext-template](https://github.com/sealdice/sealdice-js-ext-template) — 插件模板

## License

[Apache-2.0](LICENSE)
