import os
import shutil
import logging

from block_markdown import markdown_to_html_node

def copy_folder_and_contents(src, dst):
    try:
        if not os.path.exists(src):
            raise FileNotFoundError(f"Source path '{src}' does not exist")
            
        if not os.path.exists(dst):
            try:
                os.makedirs(dst)
            except PermissionError:
                raise PermissionError(f"Permission denied creating directory '{dst}'")
            except OSError as e:
                raise OSError(f"Failed to create directory '{dst}': {str(e)}")

        # Copy contents
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            
            try:
                if os.path.isdir(s):
                    copy_folder_and_contents(s, d)
                else:
                    shutil.copy2(s, d)
            except PermissionError:
                raise PermissionError(f"Permission denied accessing '{s}' or '{d}'")
            except shutil.Error as e:
                raise OSError(f"Error copying '{s}' to '{d}': {str(e)}")
                
    except Exception as e:
        logging.error(f"Failed to copy folder: {str(e)}")
        raise

def generate_page(from_path, template_path, dest_path):
    logging.info(f"Generating page from {from_path}, to {dest_path} using {template_path}")

    try:
        if not os.path.exists(from_path):
            raise FileNotFoundError(f"Source markdown file '{from_path}' does not exist")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file '{template_path}' does not exist")

        with open(from_path, "r") as file:
            markdown_content = file.read()

        with open(template_path, "r") as file:
            template_content = file.read()

        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()

        title = extract_title(markdown_content)
        template_content = template_content.replace("{{ Title }}", title)
        template_content = template_content.replace("{{ Content }}", html_content)

        dest_dir = os.path.dirname(dest_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)

        with open(dest_path, "w") as file:
            file.write(template_content)

    except Exception as e:
        logging.error(f"Error generating page: {str(e)}")
        raise

def build_site(content_dir, template_path, public_dir):
    try:
        if not os.path.exists(public_dir):
            os.makedirs(public_dir)

        static_dir = os.path.join(content_dir, "static")
        if os.path.exists(static_dir):
            static_public = os.path.join(public_dir, "static")
            copy_folder_and_contents(static_dir, static_public)

        for root, _, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.md'):
                    from_path = os.path.join(root, file)
                    rel_path = os.path.relpath(from_path, content_dir)
                    dest_path = os.path.join(
                        public_dir,
                        os.path.splitext(rel_path)[0] + '.html'
                    )
                    generate_page(from_path, template_path, dest_path)

    except Exception as e:
        logging.error(f"Error building site: {str(e)}")
        raise

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


