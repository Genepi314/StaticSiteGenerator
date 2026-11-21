from copystatic import reset_dir, copy_from_to
from gencontent import gen_page_recursive

import sys

def main() -> None:
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    reset_dir("./docs")
    copy_from_to("./static", "./docs")
    gen_page_recursive("./content", "./template.html", "./docs", basepath)

if __name__ == "__main__":
    main()