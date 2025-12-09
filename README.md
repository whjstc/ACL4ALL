# ACL4ALL - 网络配置与规则集

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

一个用于维护 Clash、Sing-box 等代理工具配置文件和规则集的仓库，支持多端设备同步和自动化订阅转换。

## 📁 目录结构

```
ACL4ALL/
├── README.md                      # 本文档
├── .gitignore                     # Git 忽略文件配置
├── LICENSE                        # 开源许可证
├── SECURITY_CHECKLIST.md          # 安全检查清单
│
├── subconverter/                  # Subconverter 配置模板
│   ├── basic.ini                  # 基础版配置（简单分组）
│   ├── advanced.ini               # 进阶版配置（完整分组 + Relay）
│   └── README.md                  # Subconverter 使用说明
│
├── rulesets/                      # 自定义规则集
│   ├── custom/                    # 自定义规则
│   │   ├── NetworkCheck.list      # 网络检测工具规则
│   │   ├── OverseasGOV.list       # 海外政府/教育网站规则
│   │   ├── Video-Pic-CDN.list     # 社媒 CDN 优先规则（图片/视频）
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
├── Shadowrocket/                  # Shadowrocket 配置与模块
│   ├── config/                    # 配置文件
│   │   ├── lazy_group.conf        # 基础版配置（官方群组精简版）
│   │   └── lazy_group_4me.conf    # 个人定制版配置
│   ├── modules/                   # .sgmodule 模块
│   │   └── VVeboFix4Shadowrocket.sgmodule
│   └── scripts/                   # 脚本
│       └── vvebo-combined.js
│
├── profiles/                      # 个人化配置与模板
│   ├── README.md
│   └── custom-nodes.yaml.example  # 自定义节点模板（不提交真实信息）
│
└── examples/                      # 示例和文档
    ├── usage.md                   # 使用指南
    ├── relay-setup.md             # Relay 使用示例
    └── pref-custom-node.yml       # 自定义节点示例
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

## 🔗 链式代理使用指南

### 什么是链式代理（Relay）？

链式代理是一种多跳代理技术，流量经过多个节点中转后到达目标网站。`advanced.ini` 已内置住宅IP链式代理支持。

**流量路径**：
```
你的设备 → 机场节点(中转) → 住宅IP节点(落地) → 目标网站
```

**使用场景**：
- ✅ 需要住宅IP地址访问特定服务（如某些流媒体、金融服务）
- ✅ 提高匿名性（目标网站看到的是住宅IP）
- ✅ 绕过数据中心IP限制

### 配置步骤

#### 1. 准备住宅IP节点信息

创建一个 **Secret Gist**（私密）存放节点配置：

访问 https://gist.github.com/，创建文件 `residential-nodes.yaml`：

```yaml
proxies:
  # 节点名称必须包含：住宅、RESIDENTIAL 或 ISP
  - name: "住宅IP-美国"
    type: socks5
    server: us-residential.example.com
    port: 1080
    username: your_username
    password: your_password
    udp: true

  - name: "RESIDENTIAL-日本"
    type: ss
    server: jp-residential.example.com
    port: 443
    cipher: aes-256-gcm
    password: your_password
    udp: true
```

**重要**：节点名称必须包含以下关键词之一才能被 `advanced.ini` 正确识别：
- `住宅`
- `RESIDENTIAL`
- `ISP`

#### 2. 获取 Gist Raw URL

保存后点击 **Raw** 按钮，复制 URL：
```
https://gist.githubusercontent.com/你的用户名/abc123.../raw/residential-nodes.yaml
```

#### 3. 使用 Subconverter 合并订阅

使用 `|` 分隔符合并机场订阅和 Gist 订阅：

```
https://subconverter.example.com/sub?target=clash&url=机场订阅URL|Gist_Raw_URL&config=https://raw.githubusercontent.com/whjstc/ACL4ALL/main/subconverter/advanced.ini
```

**完整示例**：
```
https://api.example.com/sub?target=clash&url=https://airport.com/sub/abc123|https://gist.githubusercontent.com/你的用户名/abc123.../raw/residential-nodes.yaml&config=https://raw.githubusercontent.com/whjstc/ACL4ALL/main/subconverter/advanced.ini
```

#### 4. 在客户端中使用

生成的配置会自动包含 `🔗 住宅IP` 策略组，支持链式代理的分组包括：

- 🤖 AI 服务
- 📱 社交媒体 / TikTok
- 📺 流媒体（YouTube、Netflix、Disney+、HBO、Spotify 等）
- 🎮 游戏平台
- 💻 开发工具（GitHub、Docker）
- 🍎 系统服务（苹果、微软、谷歌）
- 🐟 漏网之鱼（兜底规则）

### 工作原理

生成的配置中会包含类似的 Relay 组：

```yaml
proxy-groups:
  - name: 🔗 住宅IP
    type: relay
    proxies:
      - ♻️ 自动选择      # 第一跳：机场节点（中转）
      - 住宅IP-美国       # 第二跳：住宅IP（落地）
```

当你选择 `🔗 住宅IP` 时，流量会先经过机场节点加密，再转发到住宅IP节点，最后到达目标网站。

### 安全注意事项

**Secret Gist 安全**：
- ✅ 使用 Secret Gist（不要用 Public）
- ✅ 定期轮换 Gist URL
- ✅ 不要在公开场合分享 Gist URL
- ❌ 不要把 Gist URL 提交到公开仓库

**节点信息保护**：
- ✅ 使用强密码
- ✅ 定期更换凭据
- ✅ 监控流量异常
- ❌ 不要与他人共享住宅IP节点

### 常见问题

**Q: 为什么住宅IP节点不工作？**
- 检查节点名称是否包含关键词（`住宅`/`RESIDENTIAL`/`ISP`）
- 验证 Gist URL 是否正确
- 确认住宅IP服务商节点正常运行

**Q: 链式代理会更慢吗？**
- 是的，多一跳会增加延迟
- 建议只在必要时使用（如需要住宅IP的服务）
- 常规浏览可以直接使用机场节点

**Q: 可以添加多个住宅IP节点吗？**
- 可以，在 Gist 中添加多个节点
- Relay 组会自动匹配所有符合条件的节点
- 可以手动选择使用哪个住宅IP落地

详细示例请参考：[`examples/relay-setup.md`](examples/relay-setup.md)

---

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

## 📝 更新日志

### 2025-12-09

**链式代理优化**：
- 优化 `advanced.ini` 链式代理配置，简化并增强隐私保护
- 将服务商名称改为中性命名"住宅IP"，支持关键词匹配：`住宅`/`RESIDENTIAL`/`ISP`
- 移除地区细分的链式代理组，统一为单个 `🔗 住宅IP` relay 组
- 所有功能分组（25个）统一添加链式代理选项
- 标准化节点顺序：`香港 → 美国 → 新加坡 → 日本 → 台湾 → 韩国 → 住宅IP → 节点选择 → DIRECT`
- 修正 TikTok 组原有的顺序不一致问题
- 兜底规则"漏网之鱼"增加链式代理选项

**规则集更新**：
- 新增 `NetworkCheck.list`：网络诊断工具规则（58条）
- 新增 `OverseasGOV.list`：海外政府/教育网站规则（38条）
- 新增 `Video-Pic-CDN.list`：社交媒体 CDN 规则（50条，原 social-media-cdn.list）

**Shadowrocket 配置**：
- 新增 `lazy_group.conf`：基础版配置
- 新增 `lazy_group_4me.conf`：个人定制版，统一策略组命名为大写

**文档完善**：
- README 新增"链式代理使用指南"章节，包含完整配置流程
- 补充 Secret Gist 使用方法和安全注意事项

## 📄 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源。

## 🙏 致谢

- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) - 规则集参考
- [tindy2013/subconverter](https://github.com/tindy2013/subconverter) - 订阅转换工具
- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) - 规则集灵感

---

**Star ⭐ 本项目以支持开发！**
