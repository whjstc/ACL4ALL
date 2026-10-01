# Subconverter 配置

本目录包含订阅转换配置模板，用于生成适配不同客户端的配置文件。

## 📄 配置文件

| 文件 | 说明 | 适用场景 |
|------|------|----------|
| `basic.ini` | 基础版 | 简单地区分组、流媒体分流 |
| `advanced.ini` | 进阶版 | 完整分组、Relay 支持、AI/游戏/开发分流 |
| `Custom_Clash.ini` | 参考配置 | OpenClash 参考模板 |

## 🚀 使用方式

在 Subconverter 服务中使用远程配置：

```
https://cdn.jsdelivr.net/gh/whjstc/ACL4ALL@main/subconverter/advanced.ini
```

## 🔧 自定义配置

编辑 `.ini` 文件修改策略组或规则集，提交后等待 CDN 刷新（约 5 分钟）。

## 📝 策略组类型

- `select`: 手动选择
- `url-test`: 自动选择最低延迟
- `fallback`: 故障转移
- `relay`: 链式代理

## 相关资源

- [Subconverter 项目](https://github.com/tindy2013/subconverter)
