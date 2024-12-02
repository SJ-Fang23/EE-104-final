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

    noise_gaussian = generate_gaussian_noise(255, 255, mean=0, variance=0.1)
    noise_uniform = generate_uniform_noise(255, 255, scale=0.5, mean=0)

    # generate a white image
    img_white = Image.new('L', (255, 255), 255)
    # add noise to the white image
    img_white_gaussian = add_noise(img_white, noise_gaussian, alpha=0.5)
    img_white_uniform = add_noise(img_white, noise_uniform, alpha=0.5)

    # save the images to the output folder
    img_white_gaussian.save(os.path.join(output_folder_gaussian, "white_gaussian.jpg"))
    img_white_uniform.save(os.path.join(output_folder_uniform, "white_uniform.jpg"))

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            main_name = filename.split('_')[-1][:-4]
            img = Image.open(os.path.join(input_folder, filename))
            img_gaussian = add_noise(img, noise_gaussian, alpha=0.5)
            # save the images to the output folder
            new_filename_gaussian = f"gaussian_{main_name}.jpg"
            img_gaussian.save(os.path.join(output_folder_gaussian, new_filename_gaussian))

            img_uniform = add_noise(img, noise_uniform, alpha=0.5)
            new_filename_uniform = f"uniform_{main_name}.jpg"
            img_uniform.save(os.path.join(output_folder_uniform, new_filename_uniform))