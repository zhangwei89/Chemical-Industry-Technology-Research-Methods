<#
.SYNOPSIS
  一键推送《化工行业技术研究方法》到 GitHub 并启用 GitHub Pages 部署。

.DESCRIPTION
  用法：
    1. 在 GitHub 上创建空仓库 book1（不要勾选 README / .gitignore）
    2. 配置 SSH key（推荐）或 Personal Access Token
    3. 运行本脚本：.\deploy.ps1 -RepoUrl git@github.com:<owner>/book1.git

.PARAMETER RepoUrl
  GitHub 仓库 URL，SSH 或 HTTPS 均可。

.EXAMPLE
  .\deploy.ps1 -RepoUrl git@github.com:yourname/book1.git
  .\deploy.ps1 -RepoUrl https://github.com/yourname/book1.git
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoUrl
)

$ErrorActionPreference = "Stop"

# 切到脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host "== 1/4 检查 git 状态 ==" -ForegroundColor Cyan
git rev-parse --is-inside-work-tree 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 当前目录不是 git 仓库" -ForegroundColor Red
    exit 1
}

$status = git status --porcelain
if ($status) {
    Write-Host "✗ 有未提交改动，请先 commit：" -ForegroundColor Red
    Write-Host $status
    exit 1
}
Write-Host "✓ 工作区干净" -ForegroundColor Green

Write-Host ""
Write-Host "== 2/4 配置远程仓库 ==" -ForegroundColor Cyan
$existing = git remote get-url origin 2>$null
if ($existing) {
    Write-Host "已存在 origin: $existing"
    $confirm = Read-Host "是否替换为 $RepoUrl ? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        git remote set-url origin $RepoUrl
    }
} else {
    git remote add origin $RepoUrl
}
Write-Host "✓ origin = $RepoUrl" -ForegroundColor Green

Write-Host ""
Write-Host "== 3/4 推送到 main 分支 ==" -ForegroundColor Cyan
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 推送失败，请检查认证（SSH key / Token）" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 推送成功" -ForegroundColor Green

Write-Host ""
Write-Host "== 4/4 启用 GitHub Pages ==" -ForegroundColor Cyan
Write-Host "推送完成！接下来请：" -ForegroundColor Yellow
Write-Host "  1. 打开 https://github.com/<owner>/book1/settings/pages"
Write-Host "  2. Source 选择 'GitHub Actions'"
Write-Host "  3. 等待 Actions 跑完第一个工作流（1-2 分钟）"
Write-Host "  4. 站点上线：https://<owner>.github.io/book1/"
Write-Host ""
Write-Host "如需修改仓库信息：编辑 mkdocs.yml 中 repo_url / repo_name 字段" -ForegroundColor Gray