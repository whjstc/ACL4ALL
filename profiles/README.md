# Profiles 目录说明

本目录用于存放各平台的配置文件和自定义节点配置。

## 📁 文件说明

### `custom-nodes.yaml.example`

**用途**：自定义节点配置模板（示例文件）

**包含内容**：
- Socks5、HTTP、Shadowsocks、VMess 等多种节点类型示例
- 详细的配置参数说明
- 使用注意事项

**⚠️ 重要**：这是一个**模板文件**，不包含真实信息，可以安全提交到公开仓库。

---

## 🔒 如何安全使用自定义节点？

### 步骤 1：创建本地配置文件

```bash
# 在本地复制模板文件
cd profiles
cp custom-nodes.yaml.example custom-nodes.yaml
```

### 步骤 2：编辑配置文件

```bash
# 使用任意编辑器编辑
nano custom-nodes.yaml
# 或
vim custom-nodes.yaml
# 或使用 VSCode 等 GUI 编辑器
```

填入真实信息：

```yaml
proxies:
  - name: "Cliproxy-美国ISP"
    type: socks5
    server: 207.97.155.100      # 你的真实 IP
    port: 443                    # 你的真实端口
    username: your-real-username # 你的真实用户名
    password: your-real-password # 你的真实密码
    udp: true
```

### 步骤 3：验证 .gitignore

确认 `.gitignore` 已包含 `custom-nodes.yaml`：

```bash
cat .gitignore | grep custom-nodes.yaml
```

应该看到：
```
profiles/custom-nodes.yaml
custom-nodes.yaml
```

### 步骤 4：测试（可选）

```bash
# 测试 git 是否会忽略该文件
git status

# 应该 NOT 看到 custom-nodes.yaml 出现在未跟踪文件列表中
```

---

## 🚀 使用自定义节点

### 方法 1：本地使用（推荐）

**适用场景**：你有自建的 Subconverter 服务（Docker/VPS/NAS）

1. 将本地的 `custom-nodes.yaml` 挂载到 Subconverter 容器中：

```bash
docker run -d --name subconverter \
  -p 25500:25500 \
  -v /path/to/custom-nodes.yaml:/base/custom-nodes.yaml \
  tindy2013/subconverter:latest
```

2. 在转换时使用本地文件路径：

```
订阅链接: 机场订阅|file:///base/custom-nodes.yaml
```

---

### 方法 2：使用私有 Gist（推荐）

**适用场景**：需要跨设备同步，但不想暴露信息

1. 创建 **Secret Gist**（私有）：https://gist.github.com/
2. 上传你的 `custom-nodes.yaml`
3. 获取 Raw URL：`https://gist.githubusercontent.com/用户名/gist-id/raw/custom-nodes.yaml`
4. 在 Subconverter 中使用：

```
机场订阅|https://gist.githubusercontent.com/用户名/gist-id/raw/custom-nodes.yaml
```

**⚠️ 注意**：Gist 的 Raw URL 虽然���以猜测，但理论上可被访问。如果极度重视隐私，使用方法 1 或方法 3。

---

### 方法 3：使用私有仓库（最安全）

**适用场景**：需要版本控制和跨设备同步

1. 创建一个 **Private Repository**（私有仓库）
2. 上传 `custom-nodes.yaml` 到私有仓库
3. 使用 GitHub Token 访问：

```
机场订阅|https://用户名:ghp_token@raw.githubusercontent.com/用户名/私有仓库/main/custom-nodes.yaml
```

或者使用 GitHub CLI：

```bash
gh auth token | xargs -I {} echo "机场订阅|https://{}@raw.githubusercontent.com/用户名/私有仓库/main/custom-nodes.yaml"
```

---

## ❌ 错误示范（不要这样做！）

### ❌ 错误 1：直接提交到公开仓库

```bash
# 错误！不要这样做！
git add profiles/custom-nodes.yaml
git commit -m "添加自定义节点"
git push
```

**后果**：
- 任何人都能看到你的 IP、用户名、密码
- 你的代理账号会被盗用
- 可能导致账号被封禁

---

### ❌ 错误 2：使用公开的 jsDelivr CDN

```bash
# 错误！不要这样做！
https://cdn.jsdelivr.net/gh/用户名/ACL4ALL@main/profiles/custom-nodes.yaml
```

**后果**：
- jsDelivr 是公开 CDN，任何人都能访问
- 即使仓库是私有的，jsDelivr 也无法访问（会 404）

---

## 🔐 安全最佳实践

1. ✅ **永远不要提交包含真实信息的文件到公开仓库**
2. ✅ **使用模板文件 + .gitignore 的方式**
3. ✅ **定期检查 git 状态**：`git status`
4. ✅ **定期更换密码**
5. ✅ **使用强密码**（推荐密码管理器生成）
6. ✅ **如果不小心泄露，立即更换密码并吊销 Token**

---

## 🆘 如果不小心提交了怎么办？

### 1. 立即从 Git 历史中删除

```bash
# 从 Git 历史中完全删除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch profiles/custom-nodes.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送到远程（覆盖历史）
git push origin --force --all
git push origin --force --tags
```

或使用 BFG Repo-Cleaner（更快）：

```bash
# 安装 BFG
brew install bfg  # macOS
# 或下载：https://rtyley.github.io/bfg-repo-cleaner/

# 删除文件
bfg --delete-files custom-nodes.yaml

# 清理并推送
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push origin --force --all
```

### 2. 立即更换所有密码

- 更换代理服务商的密码
- 更换机场账号密码
- 如果使用了 GitHub Token，立即吊销

### 3. 检查是否已被滥用

- 查看代理服务商的使用记录
- 检查是否有异常流量

---

## 📖 相关文档

- [GitHub Secrets 管理](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Git 安全最佳实践](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)
- [如何从 Git 历史中删除敏感数据](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

**有问题？欢迎提交 Issue（但不要在 Issue 中暴露敏感信息）！**
