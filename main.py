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
    Generate a basic mask by detecting white/gray pixels (threshold > 200).
    Applies dilation to cover edges of the watermark area.
    
    Args:
        image: Input image as numpy array.
    
    Returns:
        Binary mask where white pixels indicate areas to inpaint.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=2)
    
    return dilated_mask


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
        print(f"✅ Using custom mask: {mask_path}")
    else:
        print("🔍 Generating automatic mask in memory...")
        mask = generate_mask(image)

    print("🪄 Applying inpainting...")
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    cv2.imwrite(output_path, result)
    print(f"✨ Success! Output saved to: {output_path}")
    return True


def process_batch(input_dir: str, output_dir: str, mask_path: str = None) -> tuple:
    """
    Process all images in a directory.
    
    Args:
        input_dir: Path to input directory.
        output_dir: Path to output directory.
        mask_path: Optional path to a custom mask image.
    
    Returns:
        Tuple of (successful_count, failed_count).
    """
    if not os.path.isdir(input_dir):
        print(f"❌ Error: Input path is not a directory: {input_dir}")
        return 0, 0
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f.lower())[1] in SUPPORTED_EXTENSIONS
    ]
    
    if not image_files:
        print(f"⚠️ No supported images found in {input_dir}")
        print(f"   Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        return 0, 0
    
    total = len(image_files)
    successful = 0
    failed = 0
    
    print(f"📦 Found {total} image(s) to process...\n")
    
    for idx, filename in enumerate(image_files, 1):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)
        
        print(f"🔄 Processing {idx}/{total}: {filename}...")
        
        success = remove_watermark(input_file, output_file, mask_path)
        
        if success:
            successful += 1
        else:
            failed += 1
            print(f"⚠️ Warning: Skipping {filename} due to error.\n")
        
        if idx < total:
            print()
    
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description="🪄 Mark Water Clean - Remove watermarks and unwanted objects from images."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input image or directory (supports .jpg, .jpeg, .png, .bmp)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to save output image or directory"
    )
    parser.add_argument(
        "-m", "--mask",
        required=False,
        help="Optional path to a custom mask image (white = areas to remove)"
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting Mark Water Clean...\n")
    
    if os.path.isdir(args.input):
        successful, failed = process_batch(args.input, args.output, args.mask)
        total = successful + failed
        
        print("\n" + "=" * 50)
        print(f"📊 Batch Processing Complete!")
        print(f"   Total: {total} | ✅ Success: {successful} | ❌ Failed: {failed}")
        print("=" * 50)
        
        if failed > 0:
            sys.exit(1)
    else:
        success = remove_watermark(args.input, args.output, args.mask)
        
        if success:
            print("\n✅ Process completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Process failed.")
            sys.exit(1)


if __name__ == "__main__":
    main()