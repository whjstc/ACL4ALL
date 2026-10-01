# ACL4ALL

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

个人网络配置与规则集维护仓库，支持 Clash、Sing-box、Shadowrocket 等工具。

## 📁 目录结构

```
ACL4ALL/
├── subconverter/          # 订阅转换配置模板
│   ├── basic.ini          # 基础版（简单分组）
│   ├── advanced.ini       # 进阶版（完整分组 + Relay）
│   └── Custom_Clash.ini   # 参考配置
│
├── rulesets/              # 自定义规则集
│   └── custom/            # 文本格式规则 (.list)
│       ├── NetworkCheck.list
│       ├── OverseasGOV.list
│       ├── Video-Pic-CDN.list
│       ├── direct.list
│       ├── proxy.list
│       └── reject.list
│
├── Shadowrocket/          # Shadowrocket 配置
│   ├── config/            # 配置文件
│   ├── modules/           # .sgmodule 模块
│   └── scripts/           # 脚本
│
├── clash/                 # Clash 配置示例
└── sing-box/              # Sing-box 配置示例
```

## 🚀 使用方式

### 订阅转换

使用任意 Subconverter 服务，远程配置填写：

```
https://cdn.jsdelivr.net/gh/whjstc/ACL4ALL@main/subconverter/advanced.ini
```

### 直接使用

下载对应平台的配置文件，手动替换节点信息即可。

## 📝 配置特性

- **basic.ini**: 基础分组（适合新手）
- **advanced.ini**: 完整分组
  - 地区分组（香港/美国/日本/新加坡/台湾/韩国）
  - 流媒体分流（Netflix/Disney+/YouTube/Spotify 等）
  - AI 服务（ChatGPT/Claude/Gemini）
  - 游戏加速（Steam/Epic/Nintendo 等）

### 链式代理

> **注意**: Clash Meta 已在 v1.19.17+ 中移除 `relay` 支持。  
> 如需链式代理，推荐使用 [Sub-Store](https://github.com/sub-store-org/Sub-Store)（支持 `dialer-proxy`，可完全替代本项目）。

### 自定义规则

编辑 `rulesets/custom/*.list` 文件，提交后等待 CDN 刷新（约 5 分钟）。

## ⚠️ 安全提示

本仓库为公开仓库，**请勿提交**：
- 机场订阅链接
- 节点详细信息
- 个人身份信息

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) - 规则集参考
- [Aethersailor/Custom_OpenClash_Rules](https://github.com/Aethersailor/Custom_OpenClash_Rules) - 配置灵感
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) - 权威分流规则集
- [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) - 域名列表社区
- [tindy2013/subconverter](https://github.com/tindy2013/subconverter) - 订阅转换工具
- [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) - 规则集参考

---

**仅供个人学习交流使用**
