import os
import ast

MEMES_DIR = "./memes"
OUTPUT_DIR = "./docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "meme_keywords.md")

def extract_keywords_from_init(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"❌ 解析失败 {file_path}: {e}")
        return []

    keywords = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'add_meme':
            for kw in node.keywords:
                if kw.arg == 'keywords' and isinstance(kw.value, ast.List):
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Str):
                            keywords.append(elt.s)
    return keywords

def find_first_image_path(subdir):
    images_dir = os.path.join(subdir, "images")
    if not os.path.isdir(images_dir):
        return None

    for file in sorted(os.listdir(images_dir)):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            return os.path.join(images_dir, file).replace("\\", "/")  # 转换为适合 Markdown 的路径

    return None

def generate_markdown_table(keywords_by_module, previews_by_module):
    lines = ["# Meme Keywords\n", "| 模块 | 关键词 | 预览 |", "|------|--------|------|"]
    for module in sorted(keywords_by_module):
        keywords = keywords_by_module[module]
        kw_str = ", ".join(keywords) if keywords else "（无）"

        # 保留模块链接
        module_link = f"[{module}](.{MEMES_DIR}/{module})"

        # 添加预览图片
        image_path = previews_by_module.get(module)
        if image_path:
            preview_img = f'<img src="{image_path}" width="100">'
        else:
            preview_img = "（无）"

        lines.append(f"| {module_link} | {kw_str} | {preview_img} |")
    return "\n".join(lines)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    keywords_by_module = {}
    previews_by_module = {}

    for folder in os.listdir(MEMES_DIR):
        subdir = os.path.join(MEMES_DIR, folder)
        init_file = os.path.join(subdir, "__init__.py")

        if os.path.isdir(subdir) and os.path.isfile(init_file):
            keywords = extract_keywords_from_init(init_file)
            keywords_by_module[folder] = keywords

            image_path = find_first_image_path(subdir)
            if image_path:
                # 转换为相对路径用于 markdown
                relative_path = os.path.relpath(image_path, OUTPUT_DIR).replace("\\", "/")
                previews_by_module[folder] = relative_path

    markdown = generate_markdown_table(keywords_by_module, previews_by_module)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ 输出完成：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
