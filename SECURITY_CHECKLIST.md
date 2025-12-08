# 提交前安全检查清单

在提交代码到 GitHub 之前，请务必检查以下项目，防止敏感信息泄露。

## ✅ 检查清单

### 1. 检查未跟踪文件

```bash
git status
```

**确保以下文件不在列表中**：
- ❌ `profiles/custom-nodes.yaml`
- ❌ 任何包含 `.secret`、`.token`、`.key` 的文件
- ❌ `subscription.txt`、`subscription.yaml` 等订阅文件

### 2. 检查已暂存文件

```bash
git diff --cached --name-only
```

**确保不包含**：
- ❌ 包含真实 IP、密码、Token 的文件
- ❌ 完整的配置文件（带节点信息）

### 3. 检查 .gitignore

```bash
cat .gitignore | grep -E "custom-nodes|subscription|secret|token"
```

**应该看到**：
```
profiles/custom-nodes.yaml
custom-nodes.yaml
subscription.txt
subscription.yaml
*.secret
*.token
*.key
```

### 4. 搜索敏感关键词

```bash
# 搜索可能的密码
git grep -i "password.*=" -- ':!*.example' ':!*.md'

# 搜索可能的 Token
git grep -i "token.*=" -- ':!*.example' ':!*.md'

# 搜索 IP 地址（排除示例文件）
git grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" -- ':!*.example' ':!*.md' ':!LICENSE'
```

**如果找到真实信息，立即检查是否应该被忽略！**

### 5. 检查提交历史

```bash
# 查看最近的提交
git log --oneline -5

# 查看具体提交的文件
git show HEAD --name-only
```

**确保没有意外提交敏感文件**。

### 6. 模拟推送（Dry Run）

```bash
git push --dry-run origin main
```

**仔细查看将要推送的内容**。

---

## 🚨 发现敏感信息？

### 如果还没有提交：

```bash
# 取消暂存
git reset HEAD <文件名>

# 或者重置所有
git reset HEAD .
```

### 如果已经提交但未推送：

```bash
# 撤销最近的提交（保留更改）
git reset --soft HEAD~1

# 或者修改最近的提交
git commit --amend
```

### 如果已经推送：

**立即参考** [`profiles/README.md`](profiles/README.md) **中的紧急处理步骤**！

---

## 📝 推荐工作流

```bash
# 1. 查看状态
git status

# 2. 只添加需要的文件（不要用 git add .）
git add subconverter/
git add rulesets/
git add README.md

# 3. 检查暂存内容
git diff --cached

# 4. 提交
git commit -m "更新配置"

# 5. 推送前再次确认
git show HEAD
git push origin main
```

---

## 🛡️ 进阶防护

### 使用 Git Hooks（推荐）

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash

# 检查是否包含敏感文件
if git diff --cached --name-only | grep -qE "custom-nodes\.yaml$|subscription\.txt$"; then
    echo "❌ 错误：检测到敏感文件！"
    echo "请检查以下文件："
    git diff --cached --name-only | grep -E "custom-nodes\.yaml$|subscription\.txt$"
    exit 1
fi

# 检查是否包含真实 IP（简单检测）
if git diff --cached | grep -qE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*password"; then
    echo "⚠️  警告：可能包含真实 IP 和密码！"
    echo "请仔细检查提交内容。"
    echo "如果确认安全，使用 git commit --no-verify 跳过检查。"
    exit 1
fi

echo "✅ 安全检查通过"
exit 0
```

启用 Hook：

```bash
chmod +x .git/hooks/pre-commit
```

### 使用 git-secrets（Google 工具）

```bash
# 安装
brew install git-secrets  # macOS
# 或 sudo apt install git-secrets  # Linux

# 配置
git secrets --install
git secrets --register-aws  # 防止提交 AWS 密钥

# 添加自定义规则
git secrets --add 'password.*=.*[a-zA-Z0-9]{8,}'
git secrets --add '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:.*@'

# 扫描历史
git secrets --scan-history
```

---

## 📖 相关资源

- [GitHub: 删除敏感数据](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [git-secrets 工具](https://github.com/awslabs/git-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

---

**安全第一！宁可多检查几次，也不要泄露密码！** 🔒
