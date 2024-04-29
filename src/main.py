from copystatic import replace_directory_contents
from generate_page import generate_page

dir_path_static = "./content"
dir_path_public = "./public"
path_template = "."

def main():
    replace_directory_contents(dir_path_public, dir_path_static)
    generate_page(dir_path_public, path_template, dir_path_public)


main()
