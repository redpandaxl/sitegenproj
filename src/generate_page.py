from pathlib import Path
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
import re
import os


def extract_title(markdown):
    # Regular expression to find a line that starts with a single '#' followed by a space
    match = re.search(r'^# ([^\n]+)', markdown, re.MULTILINE)
    if match:
        # Return the text following the '# '
        return match.group(1).strip()
    else:
        # Raise an exception if no H1 header is found
        raise ValueError("No H1 header found. All pages need a single H1 header.")
    

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Read the template file once, as it will be used for all pages
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    # Create the destination directory if it does not exist
    Path(dest_dir_path).mkdir(parents=True, exist_ok=True)

    # Walk through the directory
    for root, dirs, files in os.walk(dir_path_content):
        for file_name in files:
            if file_name.endswith('.md'):
                # Full path to the markdown file
                md_path = os.path.join(root, file_name)
                # Read the markdown file
                with open(md_path, 'r', encoding='utf-8') as md_file:
                    markdown_content = md_file.read()

                # Convert markdown to HTML
                html_content = markdown_to_html_node(markdown_content).to_html()
                title = extract_title(markdown_content)

                # Fill the template
                filled_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

                # Define the output file path
                rel_path = os.path.relpath(md_path, dir_path_content)
                html_file_path = Path(dest_dir_path) / rel_path.replace('.md', '.html')

                # Ensure the directory exists
                html_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write the output HTML file
                with open(html_file_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(filled_html)

                print(f"Generated {html_file_path} from {md_path} using {template_path}")
