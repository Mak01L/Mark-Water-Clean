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
    
    auto_mask_created = False
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
        print("🔍 Generating automatic mask...")
        mask = generate_mask(image)
        auto_mask_created = True
        temp_mask_path = "temp_mask.png"
        cv2.imwrite(temp_mask_path, mask)
        mask_path = temp_mask_path
    
    print("🪄 Applying inpainting...")
    result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cv2.imwrite(output_path, result)
    print(f"✨ Success! Output saved to: {output_path}")
    
    if auto_mask_created and os.path.exists(temp_mask_path):
        os.remove(temp_mask_path)
        print("🧹 Cleaned up temporary mask file.")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="🪄 Mark Water Clean - Remove watermarks and unwanted objects from images."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input image"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to save the output image"
    )
    parser.add_argument(
        "-m", "--mask",
        required=False,
        help="Optional path to a custom mask image (white = areas to remove)"
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting Mark Water Clean...")
    success = remove_watermark(args.input, args.output, args.mask)
    
    if success:
        print("✅ Process completed successfully!")
        sys.exit(0)
    else:
        print("❌ Process failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()