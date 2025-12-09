# Shadowrocket 模块与脚本使用说明

本目录提供适用于 iOS 的 Shadowrocket 模块与脚本，当前包含 VVebo 修复模块（修复用户主页时间线与粉丝列表显示）。

## 📁 目录结构

```
Shadowrocket/
├── modules/
│   └── VVeboFix4Shadowrocket.sgmodule
└── scripts/
    └── vvebo-combined.js
```

## 🚀 快速上手

- 导入模块
  - 模块地址：`https://raw.githubusercontent.com/whjstc/ACL4ALL/main/Shadowrocket/modules/VVeboFix4Shadowrocket.sgmodule`
  - 操作路径：Shadowrocket → 模块 → 右上角 + → 远程 → 粘贴地址 → 保存 → 启用
- 启用必要开关
  - 在首页开启：重写、脚本、HTTPS 解密 (MITM)
- 配置 MITM（首次）
  - Shadowrocket → 设置 → HTTPS 解密 → 开启 → 安装证书
  - iOS → 设置 → 通用 → 关于本机 → 证书信任 → 选择 Shadowrocket 证书 → 开启完全信任
  - 模块自动追加 MITM 主机名：`api.weibo.cn`（`hostname = %APPEND% api.weibo.cn`）
- 脚本来源
  - `https://raw.githubusercontent.com/whjstc/ACL4ALL/main/Shadowrocket/scripts/vvebo-combined.js`

## 🔧 VVebo 修复模块说明

- 功能
  - 捕获 UID：拦截 `users/show` 与 `remind/unread_count`，写入 `vvebo_uid`
  - 重定向时间线：将 `statuses/user_timeline` 重定向到 `profile/statuses/tab`，并转换参数与容器 ID
  - 重构时间线响应：将新版卡片数据扁平化为旧版 `statuses` 格式，保留 `since_id`
  - 净化粉丝列表：移除 `INTEREST_PEOPLE2`（“感兴趣的人”）干扰项，仅在 `selffans` 场景生效

- 工作机制
  - 脚本使用 Shadowrocket 持久化键值保存 UID：`$persistentStore.write(uid, "vvebo_uid")`
  - 响应重写依赖 MITM 对 `api.weibo.cn` 的 HTTPS 解密

## ✅ 验证与测试

- 打开微博 App：
  - 进入任意用户主页 → 时间线应正常显示、上下拉加载不报错
  - 打开“我的粉丝” → 列表不再显示“感兴趣的人”推荐卡片
- Shadowrocket → 日志：
  - 可看到 `[VVebo] UID已捕获`、`时间线重定向成功`、`已净化粉丝列表` 等日志

## ❓常见问题

- 时间线未重定向/空白
  - 检查是否已开启 `重写`、`脚本`、`HTTPS 解密`
  - 确认已信任 Shadowrocket 证书
  - 先触发一次 `users/show` 或 `unread_count`（进入个人页或消息页）以捕获 UID

- 粉丝列表仍有推荐卡片
  - 仅在 `selffans` 请求路径下净化，确认进入的是“我的粉丝”列表

- 与其他模块冲突
  - 若有其他模块同时改写微博接口，请仅启用一个相关模块，避免规则叠加导致不可预期行为

## 🔗 原始资源链接

- 模块（sgmodule）：`https://raw.githubusercontent.com/whjstc/ACL4ALL/main/Shadowrocket/modules/VVeboFix4Shadowrocket.sgmodule`
- 脚本（JS）：`https://raw.githubusercontent.com/whjstc/ACL4ALL/main/Shadowrocket/scripts/vvebo-combined.js`

## ⚠️ 安全提示

- 本模块不包含账号密码等敏感信息，不要在公开仓库提交任何私有节点或凭证
- 若你维护自定义模块，请避免记录或上传可识别的个人数据