# 规则集 (Rulesets)

自定义分流规则集，用于精确控制流量路由。

## 📁 目录结构

```
rulesets/
└── custom/          # 文本格式规则 (.list)
    ├── direct.list  # 直连规则
    ├── proxy.list   # 代理规则
    └── reject.list  # 拦截规则
```

## 📝 规则格式

List 格式 (.list)，适用于 Clash 和 Subconverter：

```
# 注释
DOMAIN-SUFFIX,example.com
DOMAIN-KEYWORD,google
DOMAIN,www.example.com
IP-CIDR,192.168.0.0/16
```

## 🚀 使用方法

在 Subconverter 配置中引用：

```ini
ruleset=🎯 全球直连,https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/rulesets/custom/direct.list
```

## ✏️ 自定义规则

1. 编辑对应 `.list` 文件
2. 提交到 GitHub
3. 等待 CDN 刷新（约 5 分钟）
4. 重新生成订阅

## 📚 规则类型

| 类型 | 说明 | 性能 |
|------|------|------|
| DOMAIN | 完整域名匹配 | ★★★★★ |
| DOMAIN-SUFFIX | 域名后缀匹配 | ★★★★ |
| DOMAIN-KEYWORD | 关键词匹配 | ★★★ |
| IP-CIDR | IP 段匹配 | ★★★★ |

**建议**: 优先使用 `DOMAIN` 和 `DOMAIN-SUFFIX`

## 参考资源

- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR)
- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
