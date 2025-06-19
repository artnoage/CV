#!/usr/bin/env python3
"""
Convert HTML to PDF using various methods
"""

import os
import subprocess
import sys

def check_and_install_libraries():
    """Check if required libraries are installed and provide installation instructions"""
    libraries_needed = []
    
    try:
        import weasyprint
        print("✓ WeasyPrint is installed")
    except ImportError:
        libraries_needed.append("weasyprint")
    
    try:
        import pdfkit
        print("✓ pdfkit is installed")
    except ImportError:
        libraries_needed.append("pdfkit")
    
    if libraries_needed:
        print("\nMissing libraries. Install with:")
        print(f"pip3 install {' '.join(libraries_needed)}")
        print("\nFor pdfkit, you also need wkhtmltopdf:")
        print("sudo apt-get install wkhtmltopdf  # On Ubuntu/Debian")
        print("brew install --cask wkhtmltopdf   # On macOS")
        return False
    return True

def method1_weasyprint(html_file, output_pdf):
    """Use WeasyPrint - produces smallest PDFs"""
    try:
        import weasyprint
        print(f"\nMethod 1: Converting {html_file} to {output_pdf} using WeasyPrint...")
        
        # Load HTML
        html = weasyprint.HTML(filename=html_file)
        
        # Convert to PDF with optimization
        html.write_pdf(output_pdf, optimize_size=('fonts', 'images'))
        
        # Check file size
        size = os.path.getsize(output_pdf) / 1024  # KB
        print(f"✓ Created {output_pdf} - Size: {size:.1f}KB")
        return True
    except Exception as e:
        print(f"✗ WeasyPrint failed: {e}")
        return False

def method2_pdfkit(html_file, output_pdf):
    """Use pdfkit/wkhtmltopdf"""
    try:
        import pdfkit
        print(f"\nMethod 2: Converting {html_file} to {output_pdf} using pdfkit...")
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8",
            'no-outline': None,
            'dpi': 96,
            'image-quality': 85,
            'enable-local-file-access': None
        }
        
        pdfkit.from_file(html_file, output_pdf, options=options)
        
        # Check file size
        size = os.path.getsize(output_pdf) / 1024  # KB
        print(f"✓ Created {output_pdf} - Size: {size:.1f}KB")
        return True
    except Exception as e:
        print(f"✗ pdfkit failed: {e}")
        return False

def method3_chrome_headless(html_file, output_pdf):
    """Use Chrome/Chromium in headless mode - often produces good results"""
    print(f"\nMethod 3: Converting {html_file} to {output_pdf} using Chrome headless...")
    
    # Try different Chrome executables
    chrome_paths = [
        'google-chrome',
        'chromium',
        'chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    ]
    
    chrome_cmd = None
    for path in chrome_paths:
        try:
            subprocess.run([path, '--version'], capture_output=True, check=True)
            chrome_cmd = path
            break
        except:
            continue
    
    if not chrome_cmd:
        print("✗ Chrome/Chromium not found")
        return False
    
    try:
        # Convert file path to file:// URL
        abs_path = os.path.abspath(html_file)
        file_url = f"file://{abs_path}"
        
        cmd = [
            chrome_cmd,
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + output_pdf,
            '--no-margins',
            '--print-to-pdf-no-header',
            file_url
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Check file size
        size = os.path.getsize(output_pdf) / 1024  # KB
        print(f"✓ Created {output_pdf} - Size: {size:.1f}KB")
        return True
    except Exception as e:
        print(f"✗ Chrome headless failed: {e}")
        return False

def optimize_image(image_path):
    """Optimize image using PIL if available"""
    try:
        from PIL import Image
        print(f"\nOptimizing {image_path}...")
        
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = (200, 200)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save with optimization
        output_path = image_path.replace('.jpg', '_optimized.jpg')
        img.save(output_path, 'JPEG', quality=80, optimize=True)
        
        # Check size reduction
        original_size = os.path.getsize(image_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        print(f"✓ Reduced image from {original_size:.1f}KB to {new_size:.1f}KB")
        
        return output_path
    except ImportError:
        print("PIL/Pillow not installed. Install with: pip3 install Pillow")
        return None
    except Exception as e:
        print(f"Image optimization failed: {e}")
        return None

def main():
    """Main function"""
    print("HTML to PDF Converter")
    print("=" * 50)
    
    # Check libraries
    if not check_and_install_libraries():
        print("\nTrying alternative methods...")
    
    # Files
    html_files = [
        "cv_print.html",
        "cv_print_medium.html", 
        "cv_print_optimized.html",
        "cv_print_compact.html"
    ]
    
    # First, try to optimize the image
    if os.path.exists("id.jpg"):
        optimized_image = optimize_image("id.jpg")
        if optimized_image:
            print("\nConsider updating your HTML to use id_optimized.jpg instead of id.jpg")
    
    print("\nConverting HTML files to PDF...")
    print("-" * 50)
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"Skipping {html_file} - file not found")
            continue
            
        print(f"\nProcessing {html_file}:")
        
        # Try different methods
        base_name = html_file.replace('.html', '')
        
        # Method 1: WeasyPrint (if available)
        try:
            import weasyprint
            method1_weasyprint(html_file, f"{base_name}_weasyprint.pdf")
        except ImportError:
            pass
        
        # Method 2: pdfkit (if available)
        try:
            import pdfkit
            method2_pdfkit(html_file, f"{base_name}_pdfkit.pdf")
        except ImportError:
            pass
        
        # Method 3: Chrome headless (usually available)
        method3_chrome_headless(html_file, f"{base_name}_chrome.pdf")

if __name__ == "__main__":
    main()