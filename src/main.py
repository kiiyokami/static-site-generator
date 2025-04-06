from generate_content import *

def main():
    try:
        content_dir = './content'
        template_path = './template.html'
        public_dir = './public'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        build_site(content_dir, template_path, public_dir)
        logging.info("Site built successfully")
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()