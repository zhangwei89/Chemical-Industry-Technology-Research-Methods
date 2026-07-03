from pathlib import Path

p = Path(r"D:\code\book1\01_正文\第02章_技术问题识别.md")
text = p.read_text(encoding="utf-8")

# Map of unique header line -> table caption to insert BEFORE the table
labels = [
    ("| 类型 | 典型表述 | 为什么是伪问题 |",
     "**表 2-1 伪问题四类识别**\n\n"),
    ("| 维度 | 典型指标 | 典型投诉 |",
     "**表 2-2 产品问题四维度扫描**\n\n"),
    ("| 列名 | 含义 | 示例 |",
     "**表 2-3 八列问题清单模板**\n\n"),
    ("| 紧急 \\ 严重 | 高严重（4-5） | 中严重（3） | 低严重（1-2） |",
     "**表 2-4 严重度 x 紧急度矩阵**\n\n"),
]

count = 0
for needle, caption in labels:
    if caption.strip() in text:
        print(f"已存在：{caption.strip()}")
        continue
    if needle not in text:
        print(f"!! 未找到表头: {needle[:40]}")
        continue
    text = text.replace(needle, caption + needle, 1)
    count += 1
    print(f"已添加: {caption.strip()}")

p.write_text(text, encoding="utf-8")
print(f"\n共补 {count} 个表标签")