# Rule

一组以 Surge Rule Set 为源格式的代理分流规则。仓库每天自动生成以下客户端可直接引用的格式：

- `generated/surge`：Surge Rule Set
- `generated/loon`：Loon Rule Set
- `generated/shadowrocket`：Shadowrocket Rule Set
- `generated/mihomo`：Mihomo（Clash.Meta）`classical` YAML rule-provider
- `generated/quantumult-x`：Quantumult X 远程过滤规则
- `generated/sing-box`：sing-box source rule-set JSON

此外，`upstream/Yuu518/sing-box-rules` 以 Git submodule 方式跟踪 [Yuu518/sing-box-rules](https://github.com/Yuu518/sing-box-rules/) 的 `rule_set` 分支，包括 `rule_set_site` 和 `rule_set_ip` 下的 JSON/SRS 产物。每日 Action 会推进 submodule 指针，旁边的 `sing-box-rules.UPSTREAM.json` 记录准确 commit 和文件统计。

包含上游规则的克隆方式：

```bash
git clone --recurse-submodules https://github.com/Autlin/Rule.git
```

## 自动转换

GitHub Actions 每天 `03:17 UTC`（北京时间 `11:17`）运行，也可以在 Actions 页面手动触发。转换结果只在内容变化时自动提交。

本地生成与校验：

```bash
python3 scripts/convert_rules.py
python3 scripts/sync_upstream.py --check
python3 -m unittest discover -s tests -v
python3 scripts/convert_rules.py --check
```

## 使用说明

Mihomo 文件应以 `behavior: classical`、`format: yaml` 引用。Quantumult X 文件中的 `proxy` 是默认占位策略，建议在 `filter_remote` 中使用 `force-policy` 覆盖。Surge、Loon 和 Shadowrocket 的远程规则集策略由客户端配置决定。

sing-box 的 source rule-set 不支持 `IP-ASN`，因此这类规则不会写入 sing-box JSON；所有未转换项都会列在 `generated/unsupported.json`，不会静默丢失。

源文件中偶尔夹带的策略名（例如 `DIRECT`）会被剥离，以免覆盖引用方选择的策略。`extended-matching` 只在 Surge 输出中保留；其他客户端没有完全等价的逐条选项。

## 上游声明

submodule 内容来自 [Yuu518/sing-box-rules](https://github.com/Yuu518/sing-box-rules/) 及其列出的数据源，本仓库不宣称原创或重新授权。截至接入时，上游仓库没有声明许可证；使用或再分发其中规则前，请自行确认上游及原始数据源的许可条件。同步过程只推进 `rule_set` 分支的 commit 指针，不执行上游脚本或工作流。完整来源链见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。

格式参考：[Mihomo rule-providers](https://wiki.metacubex.one/en/config/rule-providers/content/)、[Quantumult X 官方示例](https://github.com/crossutility/Quantumult-X/blob/master/filter.snippet)、[sing-box source rule-set](https://sing-box.sagernet.org/configuration/rule-set/source-format/)。
