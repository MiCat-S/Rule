# Upstream attribution

本仓库通过 `vendor/Yuu518/sing-box-rules` Git submodule 引用 `Yuu518/sing-box-rules` 的生成产物，并将其中可映射字段转换到 `rules/` 下的六个客户端目录；不宣称这些规则原创，也不对它们重新授权。以下来源根据该仓库当前 `master` 分支的构建工作流整理；工具的许可证不等于其输入数据自动获得相同许可。

| 层级 | 项目或来源 | 用途 | 已核验的许可证或状态 |
| --- | --- | --- | --- |
| 目标 | [Yuu518/sing-box-rules](https://github.com/Yuu518/sing-box-rules) | 聚合、清洗并发布 domain/IP 规则 | master、src、rule_set 分支均未发现 LICENSE |
| 直接 | [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) | geosite 域名分类基础数据 | [MIT](https://github.com/v2fly/domain-list-community/blob/master/LICENSE) |
| 直接 | [Yuu518/geoip](https://github.com/Yuu518/geoip) | IP 分类输入 | [CC-BY-SA-4.0 与 GPL-3.0](https://github.com/Yuu518/geoip/blob/master/LICENSE)；另要求 MaxMind attribution |
| 直接 | [pmkol/easymosdns](https://github.com/pmkol/easymosdns/tree/rules) | 中国域名、GFW 域名和间接 IP 数据 | 默认分支为 [GPL-3.0](https://github.com/pmkol/easymosdns/blob/main/LICENSE)；rules 分支与混合数据许可不统一 |
| 直接 | [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list) | Google/Apple 在华域名 | [WTFPL-2.0](https://github.com/felixonmars/dnsmasq-china-list/blob/master/LICENSE) |
| 直接 | [Loyalsoldier/domain-list-custom](https://github.com/Loyalsoldier/domain-list-custom) | `geolocation-!cn` 补充 | [MIT](https://github.com/Loyalsoldier/domain-list-custom/blob/master/LICENSE) |
| 直接 | [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | 广告域名 | 生成物继承多个上游许可，包含 unknown 与非商业来源 |
| 直接 | [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | 广告域名 | [GPL-3.0](https://github.com/TG-Twilight/AWAvenue-Ads-Rule/blob/main/LICENSE) |
| 直接 | [SukkaW/Surge](https://github.com/SukkaW/Surge) | CDN 与下载域名 | [AGPL-3.0](https://github.com/SukkaW/Surge/blob/master/LICENSE) |
| 工具 | [cokebar/gfwlist2dnsmasq](https://github.com/cokebar/gfwlist2dnsmasq) | 转换 GFWList | [GPL-3.0](https://github.com/cokebar/gfwlist2dnsmasq/blob/master/LICENSE) |
| 工具 | [Yuu518/rules-generate](https://github.com/Yuu518/rules-generate) / [MiCat-S/rules-generate](https://github.com/MiCat-S/rules-generate) | 原转换器及经作者允许修改的六端扁平输出版本 | [AGPL-3.0](https://github.com/MiCat-S/rules-generate/blob/master/LICENSE)，保留原许可及修改声明 |
| 架构参考 | [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) | Yuu README 所述用法及相近构建路线 | [GPL-3.0](https://github.com/Loyalsoldier/v2ray-rules-dat/blob/master/LICENSE) |
| 私有/自定义 | Yuu `src`、私有 Cloudflare R2、独立静态 URL | 自定义增删、CN 基础表及额外分类 | 无法公开核验许可或完整来源 |

关键二级来源还包括：[gfwlist/gfwlist](https://github.com/gfwlist/gfwlist)（LGPL-2.1）、[Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip) 与 MaxMind GeoLite2、[17mon/china_ip_list](https://github.com/17mon/china_ip_list)（README 声明 CC-BY-NC-SA-4.0）、[misakaio/chnroutes2](https://github.com/misakaio/chnroutes2)（LICENSE 与 README 的 CC-BY-SA 版本声明不一致）、[pexcn/daily](https://github.com/pexcn/daily)（GPL-3.0）、[bigdargon/hostsVN](https://github.com/bigdargon/hostsVN)（MIT）及未发现 LICENSE 的 [DH-Teams/DH-Geo_AS_IP_CN](https://github.com/DH-Teams/DH-Geo_AS_IP_CN)。

由于来源链中包含未声明许可、许可冲突及非商业条款，上游原始 JSON/SRS 通过 submodule 引用；`rules/` 中以 `site-`、`ip-` 开头的转换结果继续受各原始来源条款约束，不能被视为本仓库原创，也不套用单一许可证。转换器本身的 AGPL-3.0 不会自动改变输入数据或生成规则的许可状态。
