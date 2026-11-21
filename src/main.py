from copystatic import reset_dir, copy_from_to
from gencontent import gen_page_recursive

def main() -> None:
    reset_dir("./public")
    copy_from_to("./static", "./public")
    gen_page_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()