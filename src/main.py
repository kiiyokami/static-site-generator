from generate_content import *

def main():
    try:
        static_dir = './static'
        content_dir = './content'
        template_path = './template.html'
        public_dir = './public'

        copy_folder_and_contents(static_dir, public_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        generate_pages_recursive(content_dir, template_path, public_dir)
        logging.info("Site built successfully")
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()