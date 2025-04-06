from generate_content import *
import sys

def generate_page(from_path, template_path, dest_path, basepath="/"):
    logging.info(f"Generating page from {from_path}, to {dest_path} using {template_path}")

    try:
        # Read and process content
        with open(from_path, "r") as file:
            markdown_content = file.read()

        with open(template_path, "r") as file:
            template_content = file.read()

        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()

        # Replace template variables
        title = extract_title(markdown_content)
        template_content = template_content.replace("{{ Title }}", title)
        template_content = template_content.replace("{{ Content }}", html_content)
        
        # Replace base paths
        template_content = template_content.replace('href="/', f'href="{basepath}')
        template_content = template_content.replace('src="/', f'src="{basepath}')

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, "w") as file:
            file.write(template_content)

    except Exception as e:
        logging.error(f"Error generating page: {str(e)}")
        raise

def build_site(content_dir, template_path, public_dir, basepath="/"):
    try:
        if not os.path.exists(public_dir):
            os.makedirs(public_dir)

        # Copy static assets
        static_dir = os.path.join(content_dir, "static")
        if os.path.exists(static_dir):
            static_public = os.path.join(public_dir, "static")
            copy_folder_and_contents(static_dir, static_public)

        # Process markdown files
        for root, _, files in os.walk(content_dir):
            for file in files:
                if file.endswith('.md'):
                    from_path = os.path.join(root, file)
                    rel_path = os.path.relpath(from_path, content_dir)
                    dest_path = os.path.join(
                        public_dir,
                        os.path.splitext(rel_path)[0] + '.html'
                    )
                    generate_page(from_path, template_path, dest_path, basepath)

    except Exception as e:
        logging.error(f"Error building site: {str(e)}")
        raise

def main():
    try:
        basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
        static_dir = './static'
        content_dir = './content'
        template_path = './template.html'
        public_dir = './docs'

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        copy_folder_and_contents(static_dir, public_dir)
        
        build_site(content_dir, template_path, public_dir, basepath)
        
        logging.info(f"Site built successfully with basepath: {basepath}")
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()
