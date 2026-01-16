import re

def minify_css(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            css = f.read()

        # Remove comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        # Remove whitespace
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r'\s*([:;{}])\s*', r'\1', css)
        css = css.replace(';}', '}')
        
        with open(output_file, 'w') as f:
            f.write(css.strip())
            
        print(f"Minified {input_file} -> {output_file}")
        
        # Calculate savings
        orig = len(open(input_file, 'rb').read())
        new = len(open(output_file, 'rb').read())
        print(f"Size: {orig} bytes -> {new} bytes ({100 - (new/orig*100):.1f}% savings)")

    except Exception as e:
        print(f"Error minifying CSS: {e}")

if __name__ == "__main__":
    minify_css('style.css', 'style.min.css')
