# ACL4ALL - 网络配置与规则集

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

一个用于维护 Clash、Sing-box 等代理工具配置文件和规则集的仓库，支持多端设备同步和自动化订阅转换。

## 📁 目录结构

```
ACL4ALL/
├── README.md                      # 本文档
├── .gitignore                     # Git 忽略文件配置
│
├── subconverter/                  # Subconverter 配置模板
│   ├── basic.ini                  # 基础版配置（简单分组）
│   ├── advanced.ini               # 进阶版配置（完整分组 + Relay）
│   └── README.md                  # Subconverter 使用说明
│
├── rulesets/                      # 自定义规则集
│   ├── custom/                    # 自定义规则
│   │   ├── direct.list            # 直连规则
│   │   ├── proxy.list             # 代理规则
│   │   └── reject.list            # 拦截规则
│   └── providers/                 # Rule Providers (YAML 格式)
│       ├── direct.yaml            # 直连规则集
│       └── proxy.yaml             # 代理规则集
│
├── clash/                         # Clash 专用配置
│   └── config.yaml                # Clash 完整配置示例
│
├── sing-box/                      # Sing-box 专用配置
│   └── config.json                # Sing-box 配置示例
│
├── profiles/                      # 各平台配置文件
│   ├── openclash/                 # OpenClash 覆写配置
│   └── shadowrocket/              # Shadowrocket 模块
│
└── examples/                      # 示例和文档
    └── usage.md                   # 使用指南
```

## 🚀 快速开始

### 1. 使用 Subconverter 生成订阅

#### 方法 A: 使用在线转换服务

访问任意 Subconverter 网页版（如 [sub-web](https://sub.bonds.id/)），填写：

- **订阅链接**：你的机场订阅地址
- **远程配置**：选择本仓库的配置文件
  ```
  https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/subconverter/advanced.ini
  ```
- **客户端**：选择 Clash 或其他

点击生成，复制生成的订阅链接。

#### 方法 B: 自建 Subconverter（Docker）

```bash
docker run -d --name subconverter \
  -p 25500:25500 \
  tindy2013/subconverter:latest
```

访问 `http://localhost:25500` 并使用本仓库配置文件。

### 2. 各端导入订阅

| 平台 | 客户端 | 导入方式 |
|------|--------|----------|
| **路由器** | OpenClash | 订阅链接粘贴到"订阅设置" |
| **Android** | Clash Meta / CMFA | 配置 → 新建配置 → URL |
| **iOS** | Shadowrocket / Stash | 首页 + 号 → 导入订阅 |
| **Windows** | Clash Verge / CFW | Profiles → Import from URL |
| **macOS** | ClashX Pro | 配置 → 托管配置 → 管理 |

### 3. 直接使用配置文件

如果不使用 Subconverter，可以直接下载 `clash/config.yaml` 或 `sing-box/config.json`，手动替换其中的节点信息。

## 📝 配置说明

### Subconverter 配置

- **basic.ini**: 适合新手，简单分组（自动选择、香港、美国、日本等）
- **advanced.ini**: 进阶用户，包含：
  - 🌍 按国家/地区自动分组
  - 🔗 Relay 链式代理支持
  - 📺 流媒体分流（Netflix、Disney+、YouTube 等）
  - 🎮 游戏加速（Steam、Epic、Xbox 等）
  - 🤖 AI 服务（ChatGPT、Claude、Gemini 等）

### 规则集说明

- **rulesets/custom/*.list**: 文本格式规则，适用于 Clash
  ```
  # 示例：direct.list
  DOMAIN-SUFFIX,example.com
  DOMAIN-KEYWORD,company
  IP-CIDR,192.168.0.0/16
  ```

- **rulesets/providers/*.yaml**: Rule Provider 格式，性能更好
  ```yaml
  payload:
    - DOMAIN-SUFFIX,example.com
    - DOMAIN-KEYWORD,company
  ```

## 🔧 自定义配置

### 添加自定义规则

1. 编辑 `rulesets/custom/direct.list` 或其他规则文件
2. 在 `subconverter/advanced.ini` 中引用：
   ```ini
   ruleset=🎯 全球直连,https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/custom/direct.list
   ```
3. 提交到 GitHub，等待 CDN 刷新（约 5 分钟）
4. 重新生成订阅链接

### 添加新的策略组

在 `subconverter/advanced.ini` 中添加：

```ini
# 示例：添加新加坡节点组
custom_proxy_group=🇸🇬 新加坡节点`url-test`(?i)(SG|Singapore|新加坡)`http://www.gstatic.com/generate_204`300,,50

# 将该组加入主选择器
custom_proxy_group=🚀 节点选择`select`[]♻️ 自动选择`[]🇸🇬 新加坡节点`[]🇭🇰 香港节点`[]DIRECT
```

## ⚠️ 安全提示

**本仓库为公开仓库，请勿提交以下敏感信息：**

- ❌ 机场订阅链接
- ❌ 订阅 Token 或 UUID
- ❌ 节点详细信息（IP、密码、密钥）
- ❌ 个人身份信息
- ❌ **自定义节点配置文件（如 `custom-nodes.yaml`）**

✅ **只提交纯规则和配置模板！**

### 如何安全使用自定义节点？

如果你需要添加自定义节点（如住宅 IP、私有代理等）：

1. **使用模板文件**：
   ```bash
   cd profiles
   cp custom-nodes.yaml.example custom-nodes.yaml
   # 编辑 custom-nodes.yaml，填入真实信息
   ```

2. **验证 .gitignore**：
   ```bash
   # 确保 custom-nodes.yaml 不会被提交
   git status | grep custom-nodes.yaml
   # 应该看不到这个文件
   ```

3. **安全使用方式**：
   - ✅ 本地使用（自建 Subconverter）
   - ✅ 使用私有 Gist（Secret Gist）
   - ✅ 使用私有仓库 + GitHub Token
   - ❌ 不要使用公开仓库 + jsDelivr CDN

4. **详细说明**：查看 [`profiles/README.md`](profiles/README.md)

### 如果不小心泄露了怎么办？

1. **立即从 Git 历史中删除**（使用 `git filter-branch` 或 BFG）
2. **立即更换所有密码**
3. **检查是否已被滥用**

详细步骤参考：[`profiles/README.md`](profiles/README.md)

## 🔗 相关资源

- [Clash 文档](https://dreamacro.github.io/clash/)
- [Clash Meta 文档](https://wiki.metacubex.one/)
- [Sing-box 文档](https://sing-box.sagernet.org/)
- [Subconverter 项目](https://github.com/tindy2013/subconverter)
- [ACL4SSR 规则集](https://github.com/ACL4SSR/ACL4SSR)

## 📄 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源。

## 🙏 致谢

- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) - 规则集参考
- [tindy2013/subconverter](https://github.com/tindy2013/subconverter) - 订阅转换工具
- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) - 规则集灵感

---

**Star ⭐ 本项目以支持开发！**
