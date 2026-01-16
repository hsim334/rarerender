from PIL import Image
import os
import glob

# Configuration
SIZES = [400, 800, 1024]  # Widths to generate
QUALITY = 80
INPUT_DIRS = ["images"]
EXTENSIONS = ["jpg", "jpeg", "png"]

def get_images():
    files = []
    for d in INPUT_DIRS:
        for ext in EXTENSIONS:
            files.extend(glob.glob(os.path.join(d, f"*.{ext}")))
    return files

def optimize_image(path):
    if not os.path.exists(path):
        print(f"Skipping {path}, not found.")
        return

    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        base, _ = os.path.splitext(path)
        
        # 1. Convert Original to WebP (max width restricted to largest size if bigger)
        # Check original size
        w, h = img.size
        
        # If original is huge, limit it to the max defined size (e.g. 1024) or keep it if we want high res desktop
        # For this task, let's keep the original logic but ensure we have the sizes we need.
        
        # Generate responsive sizes
        for width in SIZES:
            if w > width:
                # Calculate height to maintain aspect ratio
                ratio = width / w
                new_height = int(h * ratio)
                resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                
                save_name = f"{base}-{width}w.webp"
                resized_img.save(save_name, "WEBP", quality=QUALITY)
                print(f"Generated {save_name}")
            else:
                # If image is smaller than target width, just save it as webp at original size if we haven't already
                # But usually we only want downscaled versions. 
                # Let's save a "base" webp always.
                pass

        # Always create a base WebP at original resolution (or capped at 1024 if we want to enforce limits)
        # The user seems to care about speed, so let's stick to the previous script's logic for the main file
        # plus the new sizes.
        
        base_savename = base + ".webp"
        img.save(base_savename, "WEBP", quality=QUALITY)
        print(f"Converted base: {base_savename}")
        
    except Exception as e:
        print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    print("Starting responsive image generation...")
    
    # Specific list from user request + common hero images
    target_images = [
        "images/hero-after.jpg",
        "images/hero-before.jpg",
        "images/after-3.jpg", 
        "images/after-4.jpg",
        "images/staged-outdoor-1.jpg",
        "images/staged-kitchen-1.jpg",
        "images/staged-bedroom-1.jpg" # Adding others that might be needed
    ]
    
    # Also scan directory for matching patterns if needed, but let's stick to the explicit list plus what we see in the folder
    # simpler to just walk the dir for matching filenames if we wanted to be exhaustive.
    # For now, let's process the ones we know about.
    
    for img_path in target_images:
        optimize_image(img_path)
        
    print("Done.")

