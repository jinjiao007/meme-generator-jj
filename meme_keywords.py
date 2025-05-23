import os
import ast
from datetime import datetime

MEMES_DIR = "./memes"
OUTPUT_DIR = "./docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "meme_keywords.md")

def extract_info_from_init(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"❌ 解析失败 {file_path}: {e}")
        return [], None

    keywords = []
    date_created = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'add_meme':
            for kw in node.keywords:
                if kw.arg == 'keywords' and isinstance(kw.value, ast.List):
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Str):
                            keywords.append(elt.s)
                if kw.arg == 'date_created' and isinstance(kw.value, ast.Call) and getattr(kw.value.func, 'id', '') == 'datetime':
                    args = kw.value.args
                    if len(args) >= 3 and all(isinstance(a, ast.Constant) for a in args[:3]):
                        year, month, day = args[0].value, args[1].value, args[2].value
                        date_created = datetime(year, month, day)
    return keywords, date_created

def find_first_image_path(subdir):
    images_dir = os.path.join(subdir, "images")
    if not os.path.isdir(images_dir):
        return None

    for file in sorted(os.listdir(images_dir)):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            return os.path.join(images_dir, file).replace("\\", "/")
    return None

def generate_markdown_table(modules_info):
    lines = ["| 序号 | 模块 | 关键词 | 创建日期 | 预览 |", "|------|------|--------|------------|------|"]
    for idx, (module, info) in enumerate(modules_info, 1):
        kw_str = ", ".join(info["keywords"]) if info["keywords"] else "（无）"
        module_link = f"[{module}](.{MEMES_DIR}/{module})"
        date_str = info["date_created"].strftime("%Y-%m-%d") if info["date_created"] else "未知"
        preview_img = f'<img src="{info["preview"]}" width="100">' if info["preview"] else "（无）"
        lines.append(f"| {idx} | {module_link} | {kw_str} | {date_str} | {preview_img} |")
    return "\n".join(lines)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    modules_info = []
    total_keywords = 0

    for folder in os.listdir(MEMES_DIR):
        subdir = os.path.join(MEMES_DIR, folder)
        init_file = os.path.join(subdir, "__init__.py")

        if os.path.isdir(subdir) and os.path.isfile(init_file):
            keywords, date_created = extract_info_from_init(init_file)
            total_keywords += len(keywords)

            image_path = find_first_image_path(subdir)
            relative_path = os.path.relpath(image_path, OUTPUT_DIR).replace("\\", "/") if image_path else None

            modules_info.append((
                folder,
                {
                    "keywords": keywords,
                    "date_created": date_created or datetime.min,
                    "preview": relative_path
                }
            ))

    # 按 date_created 倒序排序
    modules_info.sort(key=lambda x: x[1]["date_created"], reverse=True)

    header = f"# ✨Meme Keywords\n\n**🎈总表情数：{total_keywords}**\n"
    markdown_table = generate_markdown_table(modules_info)
    markdown = header + "\n" + markdown_table

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ 输出完成：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
