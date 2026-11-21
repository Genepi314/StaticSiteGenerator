import os, shutil

def reset_dir(destination_dir: str):

    if "static" in destination_dir or "src" in destination_dir:
        raise PermissionError("Cannot delete content of src or static directories")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)


def copy_from_to(origin_dir: str, destination_dir: str):
    # print(f"paths given : {origin_dir}, {destination_dir}")

    entries = os.listdir(origin_dir)

    for entry in entries:
        origin_path = os.path.join(origin_dir, entry)
        destination_path = os.path.join(destination_dir, entry)
        
        # print(f"paths created by joining list of entries in origin dir : {origin_path}, {destination_path}")
        
        if os.path.isfile(origin_path):
            shutil.copy(origin_path, destination_path)
        else:
            os.mkdir(destination_path)
            copy_from_to(origin_path, destination_path)