# Rule

每天自动同步并转换的代理分流规则仓库。本地规则与上游规则不再分目录，所有可用产物都直接放在 `rules/` 下对应的六个客户端目录中。

## 规则目录直达

| 客户端 | 规则目录 | 格式 |
| --- | --- | --- |
| Surge | [`rules/surge`](rules/surge/) | Rule Set `.list` |
| Loon | [`rules/loon`](rules/loon/) | Rule Set `.list` |
| Shadowrocket | [`rules/shadowrocket`](rules/shadowrocket/) | Rule Set `.list` |
| Mihomo / Clash.Meta | [`rules/mihomo`](rules/mihomo/) | `classical` rule-provider `.yaml` |
| Quantumult X | [`rules/quantumult-x`](rules/quantumult-x/) | 远程过滤规则 `.list` |
| sing-box | [`rules/sing-box`](rules/sing-box/) | source rule-set `.json` / `.srs` |

```text
rules/
├── surge/
├── loon/
├── shadowrocket/
├── mihomo/
├── quantumult-x/
└── sing-box/
```

六个客户端目录内都不再创建子目录：

- 本仓库原有规则使用原名称，例如 `ApplePush.list`、`jys-jyx.list`。
- 上游域名规则使用 `site-` 前缀，例如 `site-google.list`。
- 上游 IP 规则使用 `ip-` 前缀，例如 `ip-google.list`。

前缀只用于区分规则类型和避免同名覆盖，不代表产物被分成不同来源目录。可直接使用 Raw 地址订阅，例如：

```text
https://raw.githubusercontent.com/MiCat-S/Rule/main/rules/surge/site-google.list
```

## 自动同步和转换

[GitHub Actions](.github/workflows/convert-rules.yml) 每天 `03:17 UTC`（北京时间 `11:17`）运行，也支持在 Actions 页面手动触发。工作流会：

1. 推进 [Yuu518/sing-box-rules](https://github.com/Yuu518/sing-box-rules/) 的 `rule_set` submodule 指针；
2. 转换 [`source`](source/) 中的本地 Surge 风格规则；
3. 使用修改后的 [MiCat-S/rules-generate](https://github.com/MiCat-S/rules-generate/) 转换全部上游 JSON/SRS；
4. 运行测试和新鲜度检查，仅在内容变化时提交 `rules/`、`metadata/` 和 submodule 指针。

构建输入和报告放在 `rules/` 外，避免污染客户端目录：

| 内容 | 位置 |
| --- | --- |
| 本地源规则 | [`source`](source/) |
| 上游 submodule | [`vendor/Yuu518/sing-box-rules`](vendor/Yuu518/sing-box-rules/) |
| 转换和同步报告 | [`metadata`](metadata/) |
| 脚本 | [`scripts`](scripts/) |
| 上游来源及许可说明 | [`ATTRIBUTION.md`](ATTRIBUTION.md) |

包含上游规则的完整克隆方式：

```bash
git clone --recurse-submodules https://github.com/MiCat-S/Rule.git
```

## 转换说明

上游转换器来自作者允许修改的 [Yuu518/rules-generate](https://github.com/Yuu518/rules-generate/)，本仓库使用的修改版发布在 [MiCat-S/rules-generate](https://github.com/MiCat-S/rules-generate/)，并保留原 AGPL-3.0 许可证和修改说明。

- Surge、Loon 和 Shadowrocket 产物不写入策略，由客户端引用配置决定。
- Mihomo 文件使用 `behavior: classical` 和 `format: yaml`。
- Quantumult X 使用 `proxy` 作为占位策略，建议通过 `filter_remote` 的 `force-policy` 覆盖。
- sing-box 同时保留上游 `.json` 和 `.srs`。本地源规则里的 `IP-ASN` 无法写入 sing-box source rule-set，具体条目记录在 [`metadata/local-unsupported.json`](metadata/local-unsupported.json)。
- 上游当前有 2 个只有 `.srs`、没有 JSON 源的规则集，因此无法转换成另外五种文本格式，记录在 [`metadata/upstream-conversion.json`](metadata/upstream-conversion.json)。

源文件中夹带的策略名（例如 `DIRECT`）会被去除，以免覆盖引用方选择的策略。`extended-matching` 只在 Surge 中保留；其他客户端没有完全等价的逐条选项。

## 本地验证

```bash
git submodule update --init --recursive
python3 scripts/convert_rules.py
python3 scripts/sync_upstream.py --check
python3 -m unittest discover -s tests -v
python3 scripts/convert_rules.py --check
```

上游转换由 Action 临时检出 `MiCat-S/rules-generate` 后执行，固定到已验证的 commit，避免上游工具变化导致未经检查的输出。

## 上游声明

上游规则来自 [Yuu518/sing-box-rules](https://github.com/Yuu518/sing-box-rules/) 及其列出的数据源，本仓库不宣称这些规则原创，也不对它们重新授权。该上游仓库本身没有统一许可证，且来源链包含不同许可或未明确授权的数据；使用或再分发前请自行确认相应条款。同步仅拉取 `rule_set` 分支产物，不执行上游脚本、工作流或私有 R2。完整来源链见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。
