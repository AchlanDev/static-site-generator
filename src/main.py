
# Static Site Generator Main Module
# Run: source venv/bin/activate in ./static-site-generator

from textnode import TextNode, TextType

def main():
    print(TextNode("This is a test", TextType.LINK,  "http://example.com"))
    
if __name__ == "__main__":
    main()