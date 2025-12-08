# 使用指南

本文档详细说明如何使用 ACL4ALL 仓库的配置文件。

## 📋 目录

1. [快速开始](#快速开始)
2. [各平台导入方法](#各平台导入方法)
3. [自定义配置](#自定义配置)
4. [常见问题](#常见问题)

---

## 快速开始

### 步骤 1: 准备订阅链接

确保你已经有一个可用的机场订阅链接，格式通常如下：
```
https://example.com/api/v1/client/subscribe?token=xxxxx
```

### 步骤 2: 转换订阅

使用 Subconverter 将机场订阅转换为支持规则分流的订阅：

#### 方法 A：在线转换（推荐新手）

1. 访问 https://sub.bonds.id/
2. 填写以下信息：
   - **订阅链接**: 粘贴你的机场订阅
   - **客户端**: 选择 `Clash` 或 `ClashMeta`
   - **远程配置**: 填入以下地址（二选一）
     ```
     基础版: https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/subconverter/basic.ini
     进阶版: https://cdn.jsdelivr.net/gh/你的用户名/ACL4ALL@main/subconverter/advanced.ini
     ```
3. 点击"生成订阅链接"
4. 复制生成的订阅链接（通常以 `https://` 开头）

#### 方法 B：自建服务（推荐隐私用户）

如果你有 VPS 或 NAS，可以自建 Subconverter：

```bash
docker run -d --name subconverter \
  --restart=always \
  -p 25500:25500 \
  tindy2013/subconverter:latest
```

然后访问 `http://你的IP:25500` 使用。

### 步骤 3: 导入到客户端

将生成的订阅链接导入到你的客户端（详见下文各平台说明）。

---

## 各平台导入方法

### 🤖 Android

#### Clash Meta for Android (CMFA)

1. 打开 CMFA
2. 点击 **配置** 标签
3. 点击右上角 **+** 号
4. 选择 **从 URL 导入**
5. 粘贴订阅链接，点击 **确定**
6. 等待下载完成，点击配置激活

**推荐设置**：
- 代理模式：**规则模式**
- 允许局域网连接：**开启**（如需共享代理）
- IPv6：根据网络环境选择

---

### 🍎 iOS

#### Shadowrocket（小火箭）

1. 打开 Shadowrocket
2. 点击首页右上角 **+** 号
3. 选择 **类型** → **Subscribe**
4. 粘贴订阅链接到 **URL** 栏
5. 点击 **完成**
6. 返回首页，选择配置文件

**注意**：Shadowrocket 会自动识别 Clash 订阅格式，无需额外设置。

#### Stash

1. 打开 Stash
2. 点击 **首页** → **新建配置**
3. 选择 **通过订阅 URL 导入**
4. 粘贴订阅链接，点击 **下载**
5. 激活配置

---

### 🪟 Windows

#### Clash Verge Rev（推荐）

1. 打开 Clash Verge
2. 点击 **订阅** 标签
3. 点击 **新建** → **远程**
4. 填写以下信息：
   - **名称**: 自定义名称（如 "我的订阅"）
   - **订阅 URL**: 粘贴订阅链接
   - **更新间隔**: 选择自动更新频率（如 1440 分钟/1 天）
5. 点击 **保存**
6. 右键订阅，点击 **更新**
7. 激活配置

**推荐设置**：
- 系统代理：**开启**
- TUN 模式：**开启**（全局接管流量）
- 开机自启：**开启**

#### Clash for Windows (CFW) - 已停止维护

1. 打开 CFW
2. 点击 **Profiles** 标签
3. 在输入框中粘贴订阅链接
4. 点击 **Download**
5. 等待下载完成，点击配置激活

---

### 🍏 macOS

#### ClashX Pro

1. 打开 ClashX Pro
2. 点击菜单栏图标
3. 选择 **配置** → **托管配置** → **管理**
4. 点击 **添加**
5. 填写以下信息：
   - **URL**: 粘贴订阅链接
   - **配置名**: 自定义名称
6. 点击 **确定**
7. 在菜单中选择该配置

**推荐设置**：
- 设置为系统代理：**开启**
- 出站模式：**规则模式**
- 开机启动：**开启**

---

### 🖥️ 路由器 - OpenClash

#### 安装 OpenClash

如果路由器尚未安装 OpenClash：

1. 确保路由器已刷 OpenWrt 固件
2. 下载 OpenClash ipk 包：https://github.com/vernesong/OpenClash/releases
3. 进入 OpenWrt 管理页面
4. **系统** → **软件包** → **上传软件包** → 选择 ipk 安装

#### 配置订阅

1. 进入 **服务** → **OpenClash** → **配置订阅**
2. 点击 **添加**
3. 填写以下信息：
   - **订阅地址**: 粘贴订阅链接
   - **订阅备注**: 自定义名称
4. 点击 **保存配置**
5. 返回主界面，点击 **更新配置** → **一键更新订阅**
6. 等待更新完成，启动 OpenClash

**推荐设置**：
- 运行模式：**Fake-IP 模式**（性能最优）
- 自定义 DNS：启用，使用 `223.5.5.5` 和 `119.29.29.29`
- 允许局域网连接：**开启**
- 定时更新订阅：**开启**（每天凌晨 4 点）

---

## 自定义配置

### 添加自定义规则

如果需要为特定域名设置规则：

1. **Fork 本仓库**到你的账号
2. 编辑 `rulesets/custom/` 下的文件：
   - `direct.list` - 直连规则
   - `proxy.list` - 代理规则
   - `reject.list` - 拦截规则
3. 按照格式添加规则：
   ```
   DOMAIN-SUFFIX,example.com
   DOMAIN-KEYWORD,keyword
   IP-CIDR,192.168.0.0/16
   ```
4. 提交更改到 GitHub
5. 等待约 5 分钟 CDN 缓存刷新
6. 重新生成订阅链接

### 修改节点分组

如果你的机场节点名称不匹配默认规则：

1. 编辑 `subconverter/advanced.ini`
2. 找到节点分组部分，修改正则表达式：
   ```ini
   ; 原规则：匹配包含"香港"或"HK"的节点
   custom_proxy_group=🇭🇰 香港节点`url-test`(港|HK|Hong Kong)`...`

   ; 如果你的机场用"香港 01"、"香港 02"格式，规则已自动匹配
   ; 如果用其他格式（如"HongKong 01"），修改为：
   custom_proxy_group=🇭🇰 香港节点`url-test`(HongKong|HK)`...`
   ```
3. 提交更改，重新生成订阅

---

## 常见问题

### Q1: 订阅更新后没有变化？

**原因**：CDN 缓存未刷新

**解决方法**：
1. 在订阅链接后加上时间戳强制刷新：
   ```
   原链接?version=20251208
   ```
2. 或者等待 5-10 分钟后再更新

---

### Q2: 节点全部显示"无可用节点"？

**原因**：节点名称不匹配分组规则

**排查步骤**：
1. 在客户端查看原始订阅（不转换）的节点名称
2. 检查 `subconverter/advanced.ini` 中的正则表达式是否匹配
3. 修改正则表达式重新生成

**示例**：
- 如果节点名为 `🇭🇰 香港 IEPL 01`，规则 `(港|HK)` 能匹配
- 如果节点名为 `HKG-01`，需要修改规则为 `(港|HK|HKG)`

---

### Q3: OpenClash 无法启动？

**常见原因**：
1. 配置文件格式错误
2. 端口冲突
3. 内存不足

**解决方法**：
1. 查看日志：**服务** → **OpenClash** → **日志**
2. 检查端口占用：`netstat -tuln | grep 7890`
3. 重启路由器
4. 降低节点数量（在 Subconverter 中设置节点限制）

---

### Q4: 如何测试规则是否生效？

**方法 1**：访问特定网站
- 直连测试：访问 `baidu.com`，应该直连
- 代理测试：访问 `google.com`，应该走代理
- 拦截测试：打开有广告的网站，广告应被拦截

**方法 2**：查看客户端日志
- Clash：点击 **日志** 标签，观察请求匹配的规则
- OpenClash：**服务** → **OpenClash** → **日志**

---

### Q5: Relay 链式代理如何工作？

**工作原理**：
```
你的设备 → 节点 A → 节点 B → 目标网站
```

**使用场景**：
- 绕过地区限制（先跳到香港，再跳到美国）
- 隐藏真实 IP（多层中转）

**注意事项**：
- 延迟会增加（节点 A 延迟 + 节点 B 延迟）
- 速度受限于最慢的节点
- 仅在 `advanced.ini` 中启用

---

### Q6: 如何添加新的流媒体规则？

**示例**：添加 HBO Max 分流

1. 在 `subconverter/advanced.ini` 中添加策略组：
   ```ini
   custom_proxy_group=🎬 HBO Max`select`[]🎥 流媒体`[]🇺🇸 美国节点
   ```

2. 添加规则集：
   ```ini
   ruleset=🎬 HBO Max,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/HBOMax/HBOMax.list
   ```

3. 提交更改，重新生成订阅

---

## 🔗 相关链接

- [Clash 文档](https://dreamacro.github.io/clash/)
- [Clash Meta 文档](https://wiki.metacubex.one/)
- [OpenClash 文档](https://github.com/vernesong/OpenClash/wiki)
- [Subconverter 文档](https://github.com/tindy2013/subconverter/blob/master/README-cn.md)

---

**遇到问题？欢迎提交 [Issue](https://github.com/你的用户名/ACL4ALL/issues)！**
