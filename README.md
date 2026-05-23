# Codex Router

Codex Router 是一个本地运行的代码智能体 CLI。它保留 Codex 的 agent、tool、MCP、计划、审批、沙箱、补丁和多轮上下文能力，同时把默认模型路径切换到阿里云百炼 DashScope 的 OpenAI 兼容接口。

当前重点验证模型是 `qwen3.6-plus`。后续 `deepseekV4`、`kimi2.6`、`glm5.1`、`mimo` 等模型只要在百炼兼容模式中可用，就可以通过同一套 Codex Router 能力接入。

```shell
npm install -g @zhang3f/codexrouter
```

安装后运行：

```shell
coder
```

Codex Router 默认使用 `~/.codexrouter`，不会污染你已有的 `~/.codex` 配置。

## 快速开始

设置百炼 API Key：

```shell
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

用 Qwen 运行一次非交互任务：

```shell
coder exec -m qwen3.6-plus -c model_provider=qwen "阅读当前项目并总结它的主要模块。"
```

如果要进入交互式 TUI：

```shell
coder -m qwen3.6-plus -c model_provider=qwen
```

内置 Qwen Provider 使用：

```text
https://dashscope.aliyuncs.com/compatible-mode/v1
```

如需使用百炼较长的 app protocol 兼容地址，也可以在 `~/.codexrouter/config.toml` 中自定义 provider。

## 它解决什么问题

很多代码智能体强依赖某个海外模型或某个云端产品形态。Codex Router 的目标更窄也更直接：保留 Codex 的工程能力，只替换模型供应商。

这让团队可以在本地代码库中继续使用熟悉的 Codex agent/tool 工作流，同时把推理请求路由到百炼上的主流国产模型。

适合的场景：

- 希望在国内模型平台上运行 Codex 风格代码智能体。
- 需要 shell、apply_patch、MCP、计划更新、多轮上下文等工具能力。
- 需要 CLI/TUI 形态，而不是只调用聊天 API。
- 希望隔离配置，不影响原版 Codex 或其他开发环境。

## 优势

- **保留 Codex 能力**：不是简单聊天壳，而是保留工具调用、补丁应用、审批、沙箱、多轮任务推进和 MCP。
- **百炼兼容模式优先**：内置 `qwen` provider，默认指向 DashScope OpenAI-compatible endpoint。
- **低迁移成本**：使用 `coder` 命令，配置独立在 `~/.codexrouter`。
- **面向多模型扩展**：后续模型只要满足兼容接口和工具调用要求，就能以 provider/model 方式接入。
- **本地工程语境**：在你的工作区运行，能读代码、改文件、跑测试、生成补丁。

## 劣势和边界

- 国产模型的工具调用稳定性、长上下文表现、推理格式和 Codex 原生模型并不完全一致，需要逐个模型压测。
- 百炼兼容接口并不等同于 OpenAI Responses API 的所有细节，个别事件流或工具格式需要适配。
- 当前 npm 包主要面向 macOS `darwin-x64` 和 `darwin-arm64`。其他平台需要按源码构建或补齐发布包。
- 这不是 ChatGPT 云端 Codex，也不包含 OpenAI 账号权益。

## 配置示例

`~/.codexrouter/config.toml` 可写入默认模型：

```toml
model = "qwen3.6-plus"
model_provider = "qwen"

[model_providers.qwen]
qwen_enable_thinking = true
```

也可以增加自定义百炼兼容 provider：

```toml
[model_providers.dashscope-custom]
name = "DashScope Custom"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "DASHSCOPE_API_KEY"
wire_api = "responses"
```

然后运行：

```shell
coder exec -m qwen3.6-plus -c model_provider=dashscope-custom "帮我定位失败测试的根因。"
```

## English

Codex Router is a local coding-agent CLI. It keeps the Codex agent/tool stack, including shell execution, patch application, planning, approvals, sandboxing, MCP, and multi-turn context, while routing model calls to Alibaba Cloud Bailian DashScope.

The first hard validation target is `qwen3.6-plus`. Other DashScope-hosted models such as `deepseekV4`, `kimi2.6`, `glm5.1`, and `mimo` can be added through the same provider model once their compatible-mode behavior is verified.

Install:

```shell
npm install -g @zhang3f/codexrouter
```

Run:

```shell
export DASHSCOPE_API_KEY="your-dashscope-api-key"
coder exec -m qwen3.6-plus -c model_provider=qwen "Inspect this repository and summarize the main modules."
```

Why it exists:

- Keep Codex-style local agent workflows while changing the model backend.
- Use DashScope OpenAI-compatible mode without rewriting the CLI workflow.
- Keep configuration isolated under `~/.codexrouter`.
- Preserve tool use, file edits, tests, MCP, and multi-step coding loops.

Tradeoffs:

- Model behavior is not identical across providers, especially for tool calls and long tasks.
- Each new domestic model needs real pressure testing before being treated as production-ready.
- The current npm distribution is focused on macOS platform packages.

## 日本語

Codex Router はローカルで動作するコーディングエージェント CLI です。Codex の agent/tool、shell 実行、patch 適用、計画、承認、sandbox、MCP、多ターン文脈を維持しながら、モデル呼び出しを Alibaba Cloud Bailian DashScope に切り替えます。

最初の重点検証モデルは `qwen3.6-plus` です。`deepseekV4`、`kimi2.6`、`glm5.1`、`mimo` なども、DashScope の compatible mode で安定すれば同じ方式で追加できます。

インストール：

```shell
npm install -g @zhang3f/codexrouter
```

実行：

```shell
export DASHSCOPE_API_KEY="your-dashscope-api-key"
coder exec -m qwen3.6-plus -c model_provider=qwen "このリポジトリの主要モジュールを要約してください。"
```

強み：

- Codex のローカルエージェント体験を保ちながら、モデルだけを切り替えられます。
- `~/.codexrouter` を使うため、既存の Codex 設定と分離できます。
- CLI/TUI、ツール呼び出し、ファイル編集、テスト実行、MCP を同じ流れで扱えます。

注意点：

- モデルごとに tool calling と長いタスクの安定性が異なります。
- OpenAI の Codex クラウドサービスではありません。
- 現在の npm 配布は主に macOS 向けです。

## 한국어

Codex Router는 로컬에서 실행되는 코딩 에이전트 CLI입니다. Codex의 agent/tool, shell 실행, patch 적용, 계획, 승인, sandbox, MCP, 멀티턴 문맥 기능을 유지하면서 모델 호출을 Alibaba Cloud Bailian DashScope로 라우팅합니다.

우선 검증 대상 모델은 `qwen3.6-plus`입니다. `deepseekV4`, `kimi2.6`, `glm5.1`, `mimo` 등도 DashScope compatible mode에서 안정성이 확인되면 같은 provider 방식으로 연결할 수 있습니다.

설치:

```shell
npm install -g @zhang3f/codexrouter
```

실행:

```shell
export DASHSCOPE_API_KEY="your-dashscope-api-key"
coder exec -m qwen3.6-plus -c model_provider=qwen "이 저장소의 주요 모듈을 요약해 주세요."
```

장점:

- Codex 스타일의 로컬 에이전트 워크플로를 유지하면서 모델 백엔드만 바꿀 수 있습니다.
- 설정은 `~/.codexrouter`에 저장되어 기존 Codex 환경과 분리됩니다.
- 도구 호출, 파일 수정, 테스트 실행, MCP, 다단계 작업 루프를 그대로 사용할 수 있습니다.

한계:

- 모델마다 도구 호출과 긴 작업 처리 품질이 다릅니다.
- 새 모델은 실제 agent/tool 압력 테스트 후 사용하는 것이 안전합니다.
- 현재 npm 배포는 macOS 패키지 중심입니다.

## License

Apache-2.0. See [LICENSE](LICENSE).
