
import cv2
import pywt
import numpy as np

def dwt_image(image_path, output_path):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Ensure that the image dimensions are a power of 2 for the DWT
    rows, cols = img.shape
    new_rows = cv2.getOptimalDFTSize(rows)
    new_cols = cv2.getOptimalDFTSize(cols)
    padded_img = cv2.copyMakeBorder(img, 0, new_rows - rows, 0, new_cols - cols, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Perform the 2D Discrete Wavelet Transform
    coeffs = pywt.dwt2(padded_img, 'haar')

    # Extract LH (low-pass), LL (low-pass), HL (high-pass), HH (high-pass) bands
    LL, (LH, HL, HH) = coeffs

    # Save the bands as separate images
    cv2.imwrite(output_path + "_LL.png", LL)
    cv2.imwrite(output_path + "_LH.png", LH)
    cv2.imwrite(output_path + "_HL.png", HL)
    cv2.imwrite(output_path + "_HH.png", HH)

if __name__ == "__main__":
    # Take image path as input from the user
    input_image_path = input("Enter the path to your input image: ")

    # Verify that the input image path is valid
    try:
        image = cv2.imread(input_image_path)
        if image is None:
            raise FileNotFoundError("File not found or invalid image format.")
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Take output path as input from the user
    output_image_path = input("Enter the path to save the result: ")

    # Perform DWT and save the bands
    dwt_image(input_image_path, output_image_path)