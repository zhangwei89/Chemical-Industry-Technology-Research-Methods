import re
from pathlib import Path

CHAPTERS = [
    Path(r"D:\code\book1\01_正文\第01章_化工技术研究概述.md"),
    Path(r"D:\code\book1\01_正文\第02章_技术问题识别.md"),
]

FORBIDDEN = ["不言而喻", "在当今时代", "随着科技发展", "未来可期", "yyds", "绝绝子", "我坚信", "总而言之"]

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

def fmt(label, ok, detail=""):
    mark = "[PASS]" if ok else "[WARN]"
    return f"  {mark} {label}  {detail}"

print("=" * 70)
print("  第 1-2 章  交付自检报告")
print("=" * 70)

for ch in CHAPTERS:
    r = check_chapter(ch)
    print()
    print(f"## {r['file']}")
    print()
    print(f"  字数（去换行）: {r['chars']}")
    print(f"  节数: {r['sections']}")
    print(f"  图（含 mermaid）: {r['figures']}")
    print(f"  表（markdown 表格）: {r['tables']}")
    print(f"  案例: {r['cases']}")
    print(f"  参考文献: {sorted(r['refs'], key=int)}")
    print(f"  文内引用: {sorted(r['inline_cites'], key=int)}")
    print()
    print("  基础项：")
    print(fmt("字数 7000-9500", 7000 <= r["chars"] <= 9500, f"实际 {r['chars']}"))
    print(fmt("节数 6-8 节", 6 <= r["sections"] <= 8, f"实际 {r['sections']}"))
    print(fmt("图+表 >= 6 张", r["figures"] + r["tables"] >= 6, f"实际 {r['figures'] + r['tables']}"))
    print(fmt("案例 >= 5 个", r["cases"] >= 5, f"实际 {r['cases']}"))
    print(fmt("参考文献 >= 5 条", len(r["refs"]) >= 5, f"实际 {len(r['refs'])} 条"))
    print()
    print("  引用闭合：")
    only_inline = r["inline_cites"] - r["refs"]
    only_refs = r["refs"] - r["inline_cites"]
    if not only_inline:
        print(fmt("无悬空引用", True))
    else:
        print(fmt("悬空引用", False, f"文内 {sorted(only_inline, key=int)} 在文末无条目"))
    if not only_refs:
        print(fmt("无冗余条目", True))
    else:
        print(fmt("冗余条目", False, f"文末 {sorted(only_refs, key=int)} 在文内未引用"))
    print()
    print("  风格检查：")
    if not r["forbidden"]:
        print(fmt("无禁用词", True))
    else:
        print(fmt("发现禁用词", False, f"含 {r['forbidden']}"))

print()
print("=" * 70)
print("  两章整体一致性")
print("=" * 70)
chs = [check_chapter(c) for c in CHAPTERS]
all_forbidden = set()
for c in chs:
    all_forbidden.update(c["forbidden"])
print(f"  累计禁用词: {all_forbidden if all_forbidden else '无'}")
print(f"  平均字数: {sum(c['chars'] for c in chs) // len(chs)}")
print(f"  平均图+表: {sum(c['figures'] + c['tables'] for c in chs) // len(chs)}")
print(f"  平均案例: {sum(c['cases'] for c in chs) // len(chs)}")