# Rule

一组以 Surge Rule Set 为源格式的代理分流规则。仓库每天自动生成以下客户端可直接引用的格式：

- `generated/surge`：Surge Rule Set
- `generated/loon`：Loon Rule Set
- `generated/shadowrocket`：Shadowrocket Rule Set
- `generated/mihomo`：Mihomo（Clash.Meta）`classical` YAML rule-provider
- `generated/quantumult-x`：Quantumult X 远程过滤规则
- `generated/sing-box`：sing-box source rule-set JSON

## 自动转换

GitHub Actions 每天 `03:17 UTC`（北京时间 `11:17`）运行，也可以在 Actions 页面手动触发。转换结果只在内容变化时自动提交。

本地生成与校验：

```bash
python3 scripts/convert_rules.py
python3 -m unittest discover -s tests -v
python3 scripts/convert_rules.py --check
```

## 使用说明

Mihomo 文件应以 `behavior: classical`、`format: yaml` 引用。Quantumult X 文件中的 `proxy` 是默认占位策略，建议在 `filter_remote` 中使用 `force-policy` 覆盖。Surge、Loon 和 Shadowrocket 的远程规则集策略由客户端配置决定。

sing-box 的 source rule-set 不支持 `IP-ASN`，因此这类规则不会写入 sing-box JSON；所有未转换项都会列在 `generated/unsupported.json`，不会静默丢失。

源文件中偶尔夹带的策略名（例如 `DIRECT`）会被剥离，以免覆盖引用方选择的策略。`extended-matching` 只在 Surge 输出中保留；其他客户端没有完全等价的逐条选项。

格式参考：[Mihomo rule-providers](https://wiki.metacubex.one/en/config/rule-providers/content/)、[Quantumult X 官方示例](https://github.com/crossutility/Quantumult-X/blob/master/filter.snippet)、[sing-box source rule-set](https://sing-box.sagernet.org/configuration/rule-set/source-format/)。
