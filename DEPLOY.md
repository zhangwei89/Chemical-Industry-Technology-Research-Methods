# 部署到 GitHub Pages — 操作指南

## 概述

本项目使用 **MkDocs + Material 主题** 构建静态文档站，通过 **GitHub Actions** 自动部署到 **GitHub Pages**。首次部署约 5-10 分钟。

## 完整流程（4 步）

### 第 1 步：在 GitHub 上创建空仓库

1. 打开 https://github.com/new
2. 填写仓库名（建议 `book1`，与本地目录同名）
3. **不要**勾选 "Add a README file" / "Add .gitignore" / "Choose a license"（这些会冲突）
4. 选 Public（GitHub Pages 免费托管必须 Public）
5. 点击 "Create repository"

### 第 2 步：配置认证

任选其一：

**方式 A：SSH key（推荐）**

```powershell
# 检查是否已有 SSH key
Get-Content ~/.ssh/id_ed25519.pub 2>$null

# 没有则生成（替换邮箱）
ssh-keygen -t ed25519 -C "your@email.com"

# 把公钥加到 GitHub：Settings → SSH and GPG keys → New SSH key
# 复制 id_ed25519.pub 内容粘贴
```

**方式 B：HTTPS + Personal Access Token**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token，勾选 `repo` + `workflow`
3. 复制 token（只显示一次）
4. 推送时用 token 作密码

### 第 3 步：运行一键推送脚本

```powershell
cd D:\code\book1

# SSH 方式
.\deploy.ps1 -RepoUrl git@github.com:<your-username>/book1.git

# HTTPS 方式
.\deploy.ps1 -RepoUrl https://github.com/<your-username>/book1.git
```

脚本会自动：
- 检查 git 状态
- 配置 origin 远程
- 推送到 main 分支
- 提示后续操作

### 第 4 步：启用 GitHub Pages

1. 进入 https://github.com/<your-username>/book1/settings/pages
2. **Source** 选择 **GitHub Actions**
3. 进入 **Actions** 标签，等待第一次部署跑完（约 1-2 分钟）
4. 访问 https://<your-username>.github.io/book1/ — 站点上线！

## 修改仓库信息

部署后需更新 `mkdocs.yml` 中的占位符（搜索 `<owner>`）：

```yaml
repo_name: book1
repo_url: https://github.com/<your-username>/book1
edit_uri: edit/main/01_正文/
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/<your-username>/book1
      name: GitHub 仓库
```

改完提交：

```powershell
git add mkdocs.yml
git commit -m "docs: 修正仓库链接"
git push
```

GitHub Actions 会自动重新构建并发布。

## 常见问题

### Q1：推送时提示 "Permission denied"

**SSH 方式**：检查 `~/.ssh/id_ed25519.pub` 是否已添加到 GitHub。
**HTTPS 方式**：检查 token 是否有效、是否勾选 `repo` 权限。

### Q2：GitHub Actions 部署失败

查看 https://github.com/<your-username>/book1/actions 中的错误日志。常见原因：

- `mkdocs build` 报错：检查 `mkdocs.yml` 语法或某个 Markdown 文件标题
- 权限不足：仓库 Settings → Actions → General → Workflow permissions 选 "Read and write permissions"

### Q3：站点打开 404

- 等待 1-2 分钟，GitHub Pages 首次部署有延迟
- 确认 Settings → Pages 中 Source 是 "GitHub Actions"
- 检查 Actions 工作流是否成功

### Q4：本地预览

```powershell
# 启动实时预览（http://127.0.0.1:8000）
py -m mkdocs serve
```

修改任意 Markdown 文件后浏览器自动刷新。

### Q5：自定义域名

1. 在仓库根目录创建 `CNAME` 文件，写入你的域名（如 `book.example.com`）
2. DNS 添加 CNAME 记录指向 `<your-username>.github.io`
3. Settings → Pages → Custom domain 填写域名
4. 等待 DNS 生效（最长 24 小时）

## 部署架构

```
本地编辑 Markdown
    ↓
git push origin main
    ↓
GitHub Actions 触发 .github/workflows/deploy.yml
    ↓
ubuntu runner 安装 mkdocs + 依赖
    ↓
mkdocs build 生成 site/ 目录
    ↓
actions/upload-pages-artifact 上传
    ↓
actions/deploy-pages 发布到 gh-pages 分支
    ↓
GitHub Pages 服务：https://<owner>.github.io/book1/
```

## 自动化优势

- 每次 push 自动构建并发布，无需手动操作
- 站点历史可在 GitHub Actions 日志中追溯
- 支持 PR Preview（如果想开启，可在 workflow 中加 `pull_request` 触发器）