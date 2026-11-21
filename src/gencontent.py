from blocks_markdown import markdown_to_html_node
import os


def extract_title(markdown):
    spl_md = markdown.split("\n")
    title = ""
    for line in spl_md:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not title:
        raise ValueError("md file must contain a Heading 1")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        page_content = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    page_content = page_content.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", html)

    folder_name = os.path.dirname(dest_path)
    if folder_name:
        os.makedirs(folder_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page_content)