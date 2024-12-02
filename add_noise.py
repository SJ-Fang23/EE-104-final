from PIL import Image
import os
from utils import *

if __name__ == "__main__":

    project_dir = os.path.dirname(os.path.realpath(__file__))
    input_folder = os.path.join(project_dir, "sample_images_processed")

    output_folder_gaussian = os.path.join(project_dir, "sample_images_noisy_gaussian")
    output_folder_uniform = os.path.join(project_dir, "sample_images_noisy_uniform")
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_gaussian):
        os.makedirs(output_folder_gaussian)

    if not os.path.exists(output_folder_uniform):
        os.makedirs(output_folder_uniform)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            main_name = os.path.splitext(filename)[1]
            img = Image.open(os.path.join(input_folder, filename))
            img_gaussian = addNoise_gaussian(img, mode='grayscale')
            # save the images to the output folder
            new_filename_gaussian = f"gaussian_{filename}"
            img_gaussian.save(os.path.join(output_folder_gaussian, new_filename_gaussian))

            img_uniform = addNoise_uniform(img)
            new_filename_uniform = f"uniform_{filename}"
            img_uniform.save(os.path.join(output_folder_uniform, new_filename_uniform))