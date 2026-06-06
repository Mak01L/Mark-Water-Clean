#!/usr/bin/env python3
"""
Mark Water Clean - CLI tool for removing watermarks and unwanted objects from images.
Uses OpenCV inpainting with automatic mask generation.
"""

import argparse
import os
import sys
import cv2
import numpy as np

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}


def generate_mask(image: np.ndarray) -> np.ndarray:
    """
    Generate a basic mask by detecting EXTREME white pixels (threshold > 240).
    Applies dilation to cover edges of the watermark area.
    Note: This is a basic fallback. Custom masks are always recommended for best results.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(mask, kernel, iterations=1)


def remove_watermark(input_path: str, output_path: str, mask_path: str = None) -> bool:
    """
    Remove watermark or unwanted object from an image using inpainting.
    
    Args:
        input_path: Path to the input image.
        output_path: Path to save the processed image.
        mask_path: Optional path to a custom mask image.
    
    Returns:
        True if successful, False otherwise.
    """
    if not os.path.exists(input_path):
        print(f"❌ Error: Input image not found: {input_path}")
        return False
    
    image = cv2.imread(input_path)
    if image is None:
        print(f"❌ Error: Could not read image. Invalid format: {input_path}")
        return False
    
    if mask_path:
        if not os.path.exists(mask_path):
            print(f"❌ Error: Mask file not found: {mask_path}")
            return False
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            print(f"❌ Error: Could not read mask file: {mask_path}")
            return False
        
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        print(f"✅ Using custom mask (optimized): {mask_path}")
    else:
        print("⚠️  WARNING: Using automatic mask detection.")
        print("💡 Note: Auto-detection only works for pure white watermarks on dark backgrounds.")
        print("💡 For colored watermarks or to protect white text, ALWAYS use a custom mask (-m).")
        mask = generate_mask(image)

    print("🪄 Applying inpainting...")
    result = cv2.inpaint(image, mask, 5, cv2.INPAINT_TELEA)
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    cv2.imwrite(output_path, result)
    print(f"✨ Success! Output saved to: {output_path}")
    return True


def process_batch(input_dir: str, output_dir: str, mask_path: str = None) -> tuple:
    """Process all images in a directory."""
    if not os.path.isdir(input_dir):
        print(f"❌ Error: Input path is not a directory: {input_dir}")
        return 0, 0
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f.lower())[1] in SUPPORTED_EXTENSIONS
    ]
    
    if not image_files:
        print(f"⚠️ No supported images found in {input_dir}")
        return 0, 0

    successful, failed = 0, 0
    print(f"📦 Found {len(image_files)} image(s) to process...\n")
    
    for idx, filename in enumerate(image_files, 1):
        print(f"🔄 Processing {idx}/{len(image_files)}: {filename}...")
        if remove_watermark(
            os.path.join(input_dir, filename),
            os.path.join(output_dir, filename),
            mask_path
        ):
            successful += 1
        else:
            failed += 1
            
    print(f"\n📊 Batch Complete! ✅ Success: {successful} | ❌ Failed: {failed}")
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description="🪄 Mark Water Clean - Remove watermarks from images"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input image or directory"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to save output"
    )
    parser.add_argument(
        "-m", "--mask",
        required=False,
        help="Optional custom mask path (RECOMMENDED for colored watermarks)"
    )
    args = parser.parse_args()

    print("🚀 Starting Mark Water Clean...\n")
    
    if os.path.isdir(args.input):
        process_batch(args.input, args.output, args.mask)
    else:
        remove_watermark(args.input, args.output, args.mask)


if __name__ == "__main__":
    main()