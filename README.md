# 化工行业技术研究方法 — Action-System 主题

这本书用的是 **MkDocs Material**，不是 docsify。
我们不动 markdown 源文件，只调整 **主题颜色** 和 **CSS 覆盖**。

## 使用方式

把这两个文件拷回仓库根目录：

```
mkdocs.yml                        -> 仓库根
docs/stylesheets/extra.css       -> docs/stylesheets/
```

然后本地：

```bash
pip install mkdocs-material
mkdocs serve   # 本地预览
mkdocs gh-deploy --force  # 部署到 GitHub Pages
```

## 已做的改动

`mkdocs.yml`：
- `theme.palette.primary` / `accent` 全部改为 `red`
- 字体改为 `Noto Sans SC` / `JetBrains Mono`，与 Action-System 对齐
- 加上 `content.code.copy`、`navigation.tabs.sticky`、`search.share` 等增强

`docs/stylesheets/extra.css`：
- 主色 `--md-primary-fg-color` 等所有 primary/accent 变量覆盖为 `#c0392b`
- 标题颜色：H1 用主题红、H2/H3 用暗红
- blockquote 左侧红边 + 浅红背景
- 表格表头改红、偶数行浅红
- sidebar 灰白底、header 红底