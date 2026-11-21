from copystatic import reset_dir, copy_from_to
from gencontent import generate_page

def main() -> None:
    reset_dir("./public")
    copy_from_to("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()