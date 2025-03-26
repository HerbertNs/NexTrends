#24th march 2025 10:14PM

import os
import numpy as np
from PIL import Image

def get_standard_values(reference_folder):
    """
    Checks for the average brightness, contrast, and saturation from a folder of reference images.
    Returns: dict{'avg_brightness', 'avg_contrast', 'avg_saturation'} (0-1 scale).
    Higher numbers of images may help but theres always a sweet spot.
    """
    brightness = []
    contrast = []
    saturation = []

    for filename in os.listdir(reference_folder):
        filepath = os.path.join(reference_folder, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            with Image.open(filepath) as img:
                # Convert to HSV and grayscale
                hsv = img.convert('HSV')
                h, s, v = hsv.split()
                gray = img.convert('L')

                # Calculate metrics (0-1 scale)
                brightness.append(np.mean(np.array(v)) / 255)
                contrast.append(np.std(np.array(gray)) / 127.5)
                saturation.append(np.mean(np.array(s)) / 255)

        except Exception as e:
            print(f"Skipped {filename}: {str(e)}")

    # Return averages (or defaults if no images processed)
    return {
        'avg_brightness': np.mean(brightness) if brightness else 0.5,
        'avg_contrast': np.mean(contrast) if contrast else 0.5,
        'avg_saturation': np.mean(saturation) if saturation else 0.5
    }

def score_image(image_path, standard_values, weights=None):
    if weights is None:
        weights = {'brightness': 1/3, 'contrast': 1/3, 'saturation': 1/3}

    try:
        with Image.open(image_path) as img:
            # Converting images to HSV and grayscale
            hsv = img.convert('HSV')
            _, s, v = hsv.split()
            gray = img.convert('L')

            # Calculate metrics (0-1 scale)
            brightness = np.mean(np.array(v)) / 255
            contrast = np.std(np.array(gray)) / 127.5
            saturation = np.mean(np.array(s)) / 255

            # Absolute deviations from standard
            dev_brightness = abs(brightness - standard_values['avg_brightness'])
            dev_contrast = abs(contrast - standard_values['avg_contrast'])
            dev_saturation = abs(saturation - standard_values['avg_saturation'])

            # Weighted deviation score (0-100)
            total_deviation = 100 * (
                weights['brightness'] * dev_brightness +
                weights['contrast'] * dev_contrast +
                weights['saturation'] * dev_saturation
            )
            return total_deviation

    except Exception as e:
        print(f"⚠ Error processing image: {str(e)}")
        return None

# Example Usage
if __name__ == "__main__":
    """ You can test this by having a folder full of images. Dont worry about stray files
    they're accounted to be skipped.
    """
    REFERENCE_FOLDER = ""
    standard = get_standard_values(REFERENCE_FOLDER)
    print(f"⚙  Standard Values: Brightness={standard['avg_brightness']:.2f}, "
          f"Contrast={standard['avg_contrast']:.2f}, "
          f"Saturation={standard['avg_saturation']:.2f}")

    # Step 2: Score a test image against the standard
    TEST_IMAGE = ""
    score = score_image(TEST_IMAGE, standard)
    print(f"Test Image Score: {score:.1f}/100 : a lower value is a better score.")
    print(f"IMAGE RATING:  {round(100 - score,0)} %")