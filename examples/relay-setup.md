# 链式代理配置指南

本文档说明如何将住宅 IP socks5 代理与机场订阅合并，实现链式代理。

## 🎯 目标

- ✅ 添加自定义 socks5 节点（住宅 IP）
- ✅ 命名为「Cliproxy美国」
- ✅ 实现链式代理：住宅 IP → 机场节点

---

## 📝 三种实现方法

### 方法 1：多订阅合并（推荐 ⭐⭐⭐⭐⭐）

**优点**：简单、不需要自建服务器、GitHub 直接托管

#### 步骤 1：创建自定义节点文件

在仓库中已创建 `profiles/custom-nodes.yaml`，修改内容：

```yaml
proxies:
  - name: "Cliproxy美国"
    type: socks5
    server: 你的住宅IP地址或域名
    port: 1080
    username: 用户名（如果需要认证）
    password: 密码（如果需要认证）
    udp: true
```

#### 步骤 2：提交到 GitHub

```bash
git add profiles/custom-nodes.yaml
git commit -m "添加住宅 IP 节点配置"
git push
```

#### 步骤 3：生成订阅链接

使用 Subconverter 时，订阅链接填写：

```
机场订阅链接|https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/profiles/custom-nodes.yaml
```

**示例**：
```
https://airport.com/api/v1/client/subscribe?token=xxxxx|https://cdn.jsdelivr.net/gh/whjstc/ACL4ALL@main/profiles/custom-nodes.yaml
```

⚠️ **重要**：在某些 Subconverter 网页中，需要对 `|` 进行 URL 编码，替换为 `%7C`。

#### 步骤 4：选择远程配置

远程配置填写：
```
https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/subconverter/advanced.ini
```

生成后，你会看到：
- ✅ 所有机场节点（按地区分组）
- ✅ 「Cliproxy美国」节点（独立存在）
- ✅ 链式代理组：
  - 🔗 Cliproxy链式
  - 🔗 链式-香港（Cliproxy → 香港节点）
  - 🔗 链式-日本（Cliproxy → 日本节点）
  - 🔗 链式-新加坡（Cliproxy → 新加坡节点）

---

### 方法 2：自建 Subconverter 修改配置（推荐 ⭐⭐⭐⭐）

**适用场景**：你有 PVE / NAS / VPS，已经自建了 Subconverter

#### 步骤 1：找到 Subconverter 配置文件

```bash
# Docker 方式部署的 Subconverter
docker exec -it subconverter sh
cd /base

# 直接部署的 Subconverter
cd /path/to/subconverter
```

查找 `pref.yml` 或 `pref.toml` 文件。

#### 步骤 2：编辑配置文件

在 `pref.yml` 中添加（注意缩进）：

```yaml
# 在文件顶部或 common 部分添加
prepend_insert_proxy:
  - name: "Cliproxy美国"
    type: socks5
    server: your-residential-ip.example.com
    port: 1080
    username: your-username
    password: your-password
    udp: true
```

或在 `pref.toml` 中添加：

```toml
[[prepend_insert_proxy]]
name = "Cliproxy美国"
type = "socks5"
server = "your-residential-ip.example.com"
port = 1080
username = "your-username"
password = "your-password"
udp = true
```

#### 步骤 3：重启 Subconverter

```bash
# Docker 方式
docker restart subconverter

# systemd 方式
sudo systemctl restart subconverter
```

#### 步骤 4：重新生成订阅

使用自建的 Subconverter 重新生成订阅链接，「Cliproxy美国」节点会自动添加。

---

### 方法 3：手动编辑 Clash 配置（推荐 ⭐⭐⭐）

**适用场景**：不想折腾，直接修改配置文件

#### 步骤 1：导出当前配置

在你的 Clash 客户端中，导出当前配置文件（通常是 `config.yaml`）。

#### 步骤 2：添加自定义节点

在 `proxies:` 部分添加：

```yaml
proxies:
  # 你的机场节点（已存在）
  - name: "香港 01"
    type: ss
    server: xxx
    port: xxx
    ...

  # 添加住宅 IP
  - name: "Cliproxy美国"
    type: socks5
    server: your-residential-ip.example.com
    port: 1080
    username: your-username
    password: your-password
    udp: true
```

#### 步骤 3：添加链式代理组

在 `proxy-groups:` 部分添加：

```yaml
proxy-groups:
  # 链式代理：Cliproxy → 香港节点
  - name: "🔗 链式-香港"
    type: relay
    proxies:
      - Cliproxy美国
      - 香港 01  # 替换为你实际的节点名

  # 链式代理：Cliproxy → 日本节点
  - name: "🔗 链式-日本"
    type: relay
    proxies:
      - Cliproxy美国
      - 日本 01  # 替换为你实际的节点名

  # 在主选择器中添加链式代理
  - name: "🚀 节点选择"
    type: select
    proxies:
      - 🔗 链式-香港
      - 🔗 链式-日本
      - 香港 01
      - 日本 01
      - DIRECT
```

#### 步骤 4：导入配置

将修改后的 `config.yaml` 导入到 Clash 客户端。

---

## 🔍 验证配置是否生效

### 1. 检查节点列表

在 Clash 客户端中，查看节点列表：
- ✅ 应该能看到「Cliproxy美国」
- ✅ 应该能看到「🔗 链式-香港」等链式代理组

### 2. 测试链式代理

1. 选择「🔗 链式-香港」
2. 访问 https://ipinfo.io 或 https://ip.sb
3. 应该显示香港节点的 IP（而非住宅 IP）
4. 但流量路径是：你的设备 → ���宅 IP → 香港节点 → 目标网站

### 3. 查看延迟

链式代理的延迟 = 住宅 IP 延迟 + 机场节点延迟：
- 如果住宅 IP 延迟 50ms，香港节点延迟 30ms
- 链式代理延迟约为 80ms（可能略高）

---

## 🎓 链式代理工作原理

```
┌─────────┐    ┌──────────────┐    ┌────────────┐    ┌────────────┐
│ 你的设备 │ -> │ 住宅 IP Socks5│ -> │ 机场香港节点│ -> │ 目标网站    │
└─────────┘    └──────────────┘    └────────────┘    └────────────┘
   (客户端)       (第一跳)            (第二跳)          (最终目标)
```

**特点**：
- ✅ 目标网站看到的是「机场节点的 IP」
- ✅ 机场看到的是「住宅 IP」（而非你的真实 IP）
- ✅ 适合需要隐藏真实 IP 的场景
- ⚠️ 延迟增加（两次跳转）
- ⚠️ 速度受限于最慢的一跳

---

## 📚 常见问题

### Q1: 为什么要用链式代理？

**场景 1**：隐藏真实 IP
- 你不想让机场知道你的真实 IP
- 通过住宅 IP 作为第一跳，机场只能看到住宅 IP

**场景 2**：绕过地区限制
- 某些服务限制「数据中心 IP」但允许「住宅 IP」
- 先连住宅 IP，再连机场节点，可以绕过部分检测

**场景 3**：多层加密
- 第一跳加密，第二跳再加密
- 增加流量分析的难度

### Q2: 住宅 IP 和普通代理有什么区别？

| 类型 | IP 来源 | 信誉度 | 适用场景 |
|------|---------|--------|---------|
| **住宅 IP** | 真实家庭宽带 | 高（不易被封） | 社交媒体、电商、爬虫 |
| **数据中心 IP** | 机房服务器 | 中（容易被检测） | 日常上网、流媒体 |
| **移动 IP** | 手机运营商 | 最高（几乎不会被封） | 高风险操作 |

### Q3: 链式代理会更慢吗？

**是的**，链式代理会增加延迟和降低速度：
- 延迟：两次握手，延迟叠加
- 速度：受限于最慢的一跳

**建议**：
- 普通上网：直接用机场节点
- 需要隐藏 IP：使用链式代理
- 在 Clash 中设置**策略组**，按需切换

---

## 🔧 高级配置

### 配置多个链式代理

如果你有多个住宅 IP（不同地区）：

```yaml
proxies:
  - name: "Cliproxy美国"
    type: socks5
    server: us-residential.example.com
    port: 1080

  - name: "Cliproxy英国"
    type: socks5
    server: uk-residential.example.com
    port: 1080

  - name: "Cliproxy日本"
    type: socks5
    server: jp-residential.example.com
    port: 1080
```

策略组配置：

```ini
; 链式：美国住宅 → 香港节点
custom_proxy_group=🔗 美国链-香港`relay`(Cliproxy美国)`[]🇭🇰 香港节点

; 链式：英国住宅 → 日本节点
custom_proxy_group=🔗 英国链-日本`relay`(Cliproxy英国)`[]🇯🇵 日本节点

; 链式：日本住宅 → 美国节点
custom_proxy_group=🔗 日本链-美国`relay`(Cliproxy日本)`[]🇺🇸 美国节点
```

---

## 🛡️ 安全提示

⚠️ **不要在公开仓库提交含有认证信息的文件！**

如果你的 `custom-nodes.yaml` 包含用户名和密码：
1. 使用 **私有仓库**（Private Repository）
2. 或使用 **环境变量**（通过 Subconverter 的 URL 参数传递）
3. 或只在本地使用，不提交到 GitHub

---

**有问题？欢迎提交 Issue！**
