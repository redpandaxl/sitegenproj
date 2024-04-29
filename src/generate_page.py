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
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown = find_and_read_markdown(from_path)
    template = find_and_read_template(template_path)
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    filled_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    print(f"HTML WORK {filled_html}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(f"{dest_path}/index.html", 'w', encoding='utf-8') as file:
        file.write(filled_html)
    print(f"Page successfully generated at {dest_path}")


def find_and_read_markdown(directory):
    # Walk through all files and folders in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a Markdown file
            if file.endswith('.md'):
                # Construct the full file path
                file_path = os.path.join(root, file)
                print(f"Markdown file found: {file_path}")  # Optional: Output found file path
                # Open and read the file
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                return content  # Return the content of the first Markdown file found

    # Raise an exception if no Markdown file is found
    raise FileNotFoundError("No Markdown file found in the directory.")

def find_and_read_template(directory):
    # Walk through all files and folders in the specified directory
    for root, dirs, files in os.walk(directory):
        print(f"HTML FILES: {files}")
        for file in files:
            # Check if the file is a Markdown file
            if file.endswith('.html'):
                # Construct the full file path
                file_path = os.path.join(root, file)
                print(f"HTML file found: {file_path}")  # Optional: Output found file path
                # Open and read the file
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                return content  # Return the content of the first Markdown file found

    # Raise an exception if no Markdown file is found
    raise FileNotFoundError("No HTML file found in the directory.")
