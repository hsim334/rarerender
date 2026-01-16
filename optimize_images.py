from PIL import Image
import os

images = [
    "images/hero-after.jpg",
    "images/hero-before.jpg",
    "images/after-3.jpg",
    "images/after-4.jpg",
    "images/staged-outdoor-1.jpg",
    "images/staged-kitchen-1.jpg"
]

def optimize_image(path):
    if not os.path.exists(path):
        print(f"Skipping {path}, not found.")
        return

    try:
        img = Image.open(path)
        # Convert to RGB if necessary (e.g. if PNG with alpha, though these are JPGs)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Create output path
        base, _ = os.path.splitext(path)
        savename = base + ".webp"
        
        # Save as WebP
        # We keep original resolution as discussed (1024px is good for retina desktop)
        # Quality 80 is a good balance
        img.save(savename, "WEBP", quality=80)
        
        original_size = os.path.getsize(path) / 1024
        new_size = os.path.getsize(savename) / 1024
        print(f"Optimized {path}: {original_size:.1f}KB -> {new_size:.1f}KB ({100 - (new_size/original_size*100):.1f}% savings)")
        
    except Exception as e:
        print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    print("Starting image optimization...")
    for img in images:
        optimize_image(img)
    print("Done.")
