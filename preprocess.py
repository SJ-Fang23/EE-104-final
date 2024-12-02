from PIL import Image
import os

def preprocess_images(input_folder, output_folder):
    '''
    Converts images in input_folder to grayscale, resizes them to 255x255, and saves them in output_folder.
    '''
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = Image.open(os.path.join(input_folder, filename))
            
            img = img.convert('L')
            
            img = img.resize((255, 255))
            
            basename = os.path.basename(filename)
            name, ext = os.path.splitext(basename)
            output_filename = f"processed_{name}.jpg"
            
            img.save(os.path.join(output_folder, output_filename))


file_dir = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(file_dir, "sample_photos_raw")
output_folder = os.path.join(file_dir, "sample_images_processed")
preprocess_images(input_folder, output_folder)
