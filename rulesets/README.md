# 规则集 (Rulesets)

本目录包含自定义的分流规则集，用于精确控制流量路由。

## 📁 目录结构

```
rulesets/
├── custom/          # 自定义规则（文本格式）
│   ├── direct.list  # 直连规则
│   ├── proxy.list   # 代理规则
│   └── reject.list  # 拦截规则
└── providers/       # Rule Providers（YAML 格式）
    ├── direct.yaml  # 直连规则集
    └── proxy.yaml   # 代理规则集
```

## 📝 规则格式说明

### 1. List 格式 (`.list` 文件)

适用于 **Clash** 和 **Subconverter**。

#### 语法规则

```
# 注释行以 # 开头

# 域名后缀匹配
DOMAIN-SUFFIX,example.com

# 域名关键词匹配
DOMAIN-KEYWORD,google

# 完整域名匹配
DOMAIN,www.example.com

# IP-CIDR 匹配
IP-CIDR,192.168.0.0/16

# IP-CIDR6 匹配（IPv6）
IP-CIDR6,2001:db8::/32
```

#### 示例

```
# 直连规则示例
DOMAIN-SUFFIX,baidu.com
DOMAIN-SUFFIX,qq.com
IP-CIDR,192.168.0.0/16

# 代理规则示例
DOMAIN-SUFFIX,google.com
DOMAIN-SUFFIX,youtube.com
DOMAIN-KEYWORD,facebook

# 拦截规则示例
DOMAIN-SUFFIX,ads.example.com
DOMAIN-KEYWORD,adservice
```

---

### 2. YAML 格式 (`.yaml` 文件)

适用于 **Clash Premium / Meta** 的 **Rule Provider** 功能。

#### 语法规则

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
  - DOMAIN-KEYWORD,google
  - DOMAIN,www.example.com
  - IP-CIDR,192.168.0.0/16
  - IP-CIDR6,2001:db8::/32
```

#### 示例

```yaml
# direct.yaml - 直连规则
payload:
  - DOMAIN-SUFFIX,baidu.com
  - DOMAIN-SUFFIX,qq.com
  - IP-CIDR,192.168.0.0/16
  - IP-CIDR,10.0.0.0/8
```

---

## 🚀 使用方法

### 方法 1: 在 Subconverter 中引用

在 `subconverter/advanced.ini` 中添加规则集引用：

```ini
; 使用 jsDelivr CDN 加速（推荐）
ruleset=🎯 全球直连,https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/custom/direct.list
ruleset=🚀 节点选择,https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/custom/proxy.list
ruleset=🛑 广告拦截,https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/custom/reject.list

; 或使用 GitHub Raw 地址
ruleset=🎯 全球直连,https://raw.githubusercontent.com/你的用户名/ACL4ALL/main/rulesets/custom/direct.list
```

---

### 方法 2: 在 Clash 配置中使用 Rule Provider

在 `clash/config.yaml` 中添加：

```yaml
rule-providers:
  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/providers/direct.yaml"
    path: ./providers/direct.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/providers/proxy.yaml"
    path: ./providers/proxy.yaml
    interval: 86400

rules:
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,PROXY
  - MATCH,PROXY
```

---

## ✏️ 自定义规则

### 添加新规则

1. **编辑对应文件**：
   - 需要直连的域名 → `custom/direct.list`
   - 需要代理的域名 → `custom/proxy.list`
   - 需要拦截的域名 → `custom/reject.list`

2. **按照格式添加**：
   ```
   DOMAIN-SUFFIX,example.com
   ```

3. **提交到 GitHub**：
   ```bash
   git add rulesets/
   git commit -m "添加自定义规则"
   git push
   ```

4. **等待 CDN 刷新**（约 5-10 分钟）

5. **重新生成订阅链接**

---

### 规则优先级

**Clash 规则匹配顺序**：从上到下，匹配第一条后停止。

**建议顺序**：
1. 局域网直连（最高优先级）
2. 广告拦截
3. 自定义规则
4. 公共规则集
5. GeoIP 中国 IP
6. 兜底规则（最低优先级）

**示例**：
```yaml
rules:
  - DOMAIN-SUFFIX,local,DIRECT          # 优先级 1
  - RULE-SET,reject,REJECT              # 优先级 2
  - RULE-SET,direct,DIRECT              # 优先级 3
  - RULE-SET,proxy,PROXY                # 优先级 4
  - GEOIP,CN,DIRECT                     # 优先级 5
  - MATCH,PROXY                         # 优先级 6（兜底）
```

---

## 📚 规则类型详解

| 规则类型 | 说明 | 示例 | 性能 |
|---------|------|------|------|
| **DOMAIN** | 完整域名匹配 | `DOMAIN,www.google.com` | ⭐⭐⭐⭐⭐ 最快 |
| **DOMAIN-SUFFIX** | 域名后缀匹配 | `DOMAIN-SUFFIX,google.com` | ⭐⭐⭐⭐ 快 |
| **DOMAIN-KEYWORD** | 域名关键词匹配 | `DOMAIN-KEYWORD,google` | ⭐⭐⭐ 中等 |
| **IP-CIDR** | IP 段匹配 | `IP-CIDR,192.168.0.0/16` | ⭐⭐⭐⭐ 快 |
| **GEOIP** | 地理位置匹配 | `GEOIP,CN` | ⭐⭐ 较慢 |
| **PROCESS-NAME** | 进程名匹配 | `PROCESS-NAME,firefox` | ⭐⭐ 较慢 |

**性能建议**：
- ✅ 优先使用 `DOMAIN` 和 `DOMAIN-SUFFIX`
- ⚠️ 谨慎使用 `DOMAIN-KEYWORD`（可能误匹配）
- ⚠️ 少用 `GEOIP`（需要查表，性能开销大）

---

## 🔧 常见规则模板

### 1. 公司内网直连

```
# 公司域名
DOMAIN-SUFFIX,company.com
DOMAIN-KEYWORD,internal

# 内网 IP 段
IP-CIDR,10.0.0.0/8
IP-CIDR,172.16.0.0/12
IP-CIDR,192.168.0.0/16
```

### 2. 特定 App 代理

```
# Twitter
DOMAIN-SUFFIX,twitter.com
DOMAIN-SUFFIX,twimg.com
DOMAIN-SUFFIX,t.co

# Telegram
DOMAIN-SUFFIX,telegram.org
DOMAIN-SUFFIX,t.me
IP-CIDR,91.108.4.0/22,no-resolve
IP-CIDR,149.154.160.0/20,no-resolve
```

### 3. 广告拦截

```
# 通用广告
DOMAIN-KEYWORD,adservice
DOMAIN-KEYWORD,analytics
DOMAIN-KEYWORD,tracker

# 具体域名
DOMAIN-SUFFIX,doubleclick.net
DOMAIN-SUFFIX,googleadservices.com
```

---

## 📖 参考资源

### 常用规则集仓库

- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) - 全面的规则集合
- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) - 高性能规则
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) - 精细化分流

### 规则测试工具

- [Clash Dashboard](http://clash.razord.top/) - 查看规则匹配情况
- [YACD](https://yacd.haishan.me/) - 更现代的 Clash 面板

---

**有问题？欢迎提交 Issue！**
