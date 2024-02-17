import cv2
import pywt
import numpy as np

def swt_image(input_image_path, output_image_path, wavelet='haar', level=2):
    # Load the image
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Resize the image to the nearest power of 2
    rows, cols = img.shape
    new_rows = 2 ** int(np.ceil(np.log2(rows)))
    new_cols = 2 ** int(np.ceil(np.log2(cols)))
    resized_img = cv2.resize(img, (new_cols, new_rows))

    # Perform the 2D Stationary Wavelet Transform
    coeffs = pywt.swt2(resized_img, wavelet, level=level)

    # Extract the approximation (low-pass) and detail (high-pass) bands
    for i in range(len(coeffs)):
        A, D = coeffs[i]

        # Access the detail band from the tuple and convert its data type
        if i == 0:
            D = D[0].astype(np.float32)

            # Normalize the values in the D array to the range [0, 255]
            normalized_D = cv2.normalize(D, None, 0, 255, cv2.NORM_MINMAX)

            # Save the bands as separate images
            cv2.imwrite(output_image_path + f"_A{i}.jpg", A)
            cv2.imwrite(output_image_path + f"_D{i}.jpg", normalized_D)
        else:
            # Extract and save detail bands (D1, D2, D3)
            for j in range(len(D)):
                detail_band = D[j].astype(np.float32)
                normalized_detail_band = cv2.normalize(detail_band, None, 0, 255, cv2.NORM_MINMAX)
                cv2.imwrite(output_image_path + f"_D{i}_{j+1}.jpg", normalized_detail_band)

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

    # Perform SWT and save the bands
    swt_image(input_image_path, output_image_path)
