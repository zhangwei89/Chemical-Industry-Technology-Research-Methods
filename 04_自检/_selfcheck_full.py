"""
《化工行业技术研究方法》全本自检脚本

对所有 30 章 + 前言 + 10 附录做基础项检查：字数、节数、图、表格、案例、参考文献、禁用词。
"""
import re
from pathlib import Path

ROOT = Path(r"D:\code\book1\01_正文")

FILES = sorted(ROOT.glob("*.md"))

FORBIDDEN = [
    "不言而喻", "在当今时代", "随着科技发展", "未来可期",
    "yyds", "绝绝子", "我坚信", "总而言之"
]

def chinese_char_count(text):
    return sum(1 for c in text if c.strip() and c not in "\r\n")

def count_main_sections(text):
    return len(re.findall(r"^## \d+\.\d+\s", text, re.MULTILINE))

def count_figures(text):
    return len(re.findall(r"\*\*图\s+\d+-\d+", text))

def count_tables(text):
    return len(re.findall(r"\*\*表\s+\d+-\d+", text))

def count_cases(text):
    return len(re.findall(r"\*\*典型化案例\s+\d+-\d+\*\*", text))

def count_refs(text):
    return set(re.findall(r"^\[(\d+)\]\s", text, re.MULTILINE))

def count_inline_citations(text):
    cites = set()
    for m in re.finditer(r"\[(\d+(?:[-,\s]\d+)*)\]", text):
        for part in re.split(r"[,\s]+", m.group(1)):
            if "-" in part:
                a, b = part.split("-")
                for n in range(int(a), int(b) + 1):
                    cites.add(str(n))
            elif part.isdigit():
                cites.add(part)
    return cites

def find_forbidden(text):
    return [w for w in FORBIDDEN if w in text]

def fmt(label, ok, detail=""):
    mark = "[PASS]" if ok else "[WARN]"
    return f"  {mark} {label}  {detail}"

def check_chapter(path):
    text = path.read_text(encoding="utf-8")
    return {
        "file": path.name,
        "chars": chinese_char_count(text),
        "sections": count_main_sections(text),
        "figures": count_figures(text),
        "tables": count_tables(text),
        "cases": count_cases(text),
        "refs": count_refs(text),
        "inline_cites": count_inline_citations(text),
        "forbidden": find_forbidden(text),
    }

print("=" * 80)
print("  《化工行业技术研究方法》  全本自检报告")
print("=" * 80)
print()
print(f"  扫描文件数: {len(FILES)}")
print()

results = []
for f in FILES:
    r = check_chapter(f)
    results.append(r)

print("-" * 80)
print(f"  {'文件名':<35} {'字数':>6} {'节':>4} {'图':>4} {'表':>4} {'案例':>4} {'引用':>4} {'禁词':>4}")
print("-" * 80)

for r in results:
    refs_count = len(r["refs"])
    print(f"  {r['file']:<35} {r['chars']:>6} {r['sections']:>4} {r['figures']:>4} {r['tables']:>4} {r['cases']:>4} {refs_count:>4} {len(r['forbidden']):>4}")

print()
print("-" * 80)
print("  全本汇总")
print("-" * 80)
total_chars = sum(r["chars"] for r in results)
total_sections = sum(r["sections"] for r in results)
total_figures = sum(r["figures"] for r in results)
total_tables = sum(r["tables"] for r in results)
total_cases = sum(r["cases"] for r in results)
total_refs = sum(len(r["refs"]) for r in results)
all_forbidden = set()
for r in results:
    all_forbidden.update(r["forbidden"])

print(f"  总字数（去换行）: {total_chars:,}")
print(f"  总节数: {total_sections}")
print(f"  总图（含 mermaid）: {total_figures}")
print(f"  总表（markdown 表格）: {total_tables}")
print(f"  总案例: {total_cases}")
print(f"  总参考文献条目: {total_refs}")
print(f"  累计禁用词: {all_forbidden if all_forbidden else '无'}")

print()
print("-" * 80)
print("  引用闭合（仅 30 个正文章检查）")
print("-" * 80)
mismatches = 0
for r in results:
    if not r["file"].startswith("第"):
        continue
    only_inline = r["inline_cites"] - r["refs"]
    only_refs = r["refs"] - r["inline_cites"]
    if only_inline or only_refs:
        print(f"  [WARN] {r['file']}")
        if only_inline:
            print(f"         悬空引用: {sorted(only_inline, key=int)}")
        if only_refs:
            print(f"         冗余条目: {sorted(only_refs, key=int)}")
        mismatches += 1
if mismatches == 0:
    print(f"  [PASS] 所有 30 章引用闭合")

print()
print("=" * 80)
print("  自检完成")
print("=" * 80)