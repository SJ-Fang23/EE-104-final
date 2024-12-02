import numpy as np
from PIL import Image

#works for both single images and sets of images
def detect_image_type(images, display_type = False):
    
    # Input is a list or other iterable of images. check type of first image
    if isinstance(images, (list, tuple)):
        first_image = images[0]
        if isinstance(first_image, np.ndarray):
            if display_type == True: 
                print("NumPy: Image SET contains images stored as NumPy arrays.")
            return 'numpy_set'
        elif isinstance(first_image, Image.Image):
            if display_type == True:
                print("PIL: Image SET contains images stored as PIL images.")
            return 'pil_set'
        else:
            raise TypeError("Image SET type not recognized.")
    
    # Input is a single image
    elif isinstance(images, np.ndarray):
        if display_type == True: 
            print("NumPy: Image SINGLE is stored as a NumPy array.")
        return 'numpy_single'
    elif isinstance(images, Image.Image):
        if display_type == True:
            print("PIL: Image SINGLE is stored as a PIL image.")
        return 'pil_single'
    else:
        raise TypeError("Image SET type not recognized.")

def pil_to_numpy(images):
    '''note: this function will not harm image(s) that are already in numpy format'''
    current_type = detect_image_type(images)
        
    # Immediately return numpy images
    if current_type == 'numpy_set' or current_type == 'numpy_single':
        return images
    
    # Convert single PIL image to NumPy array
    elif current_type == 'pil_single':
        numpy_img = np.array(images).astype(np.uint8)
        return numpy_img
    
    # Convert set of PIL images to set of NumPy arrays
    elif current_type == 'pil_set':
        numpy_images = []
        for img in images:
            numpy_img = np.array(img).astype(np.uint8)
            numpy_images.append(numpy_img)
        return numpy_images
    
    else:
        print("Attempted pil_to_numpy. Image type could not be identified -- data returned unmodified.")
        return images

def numpy_to_pil(images):
    '''note: this function will not harm image(s) that are already in pil format'''
    current_type = detect_image_type(images)
    
    # Immediately return PIL images
    if current_type == 'pil_single' or current_type == 'pil_set':
        return images
    
    # Convert single NumPy array to PIL image
    elif current_type == 'numpy_single':
        pil_img = Image.fromarray(images.astype(np.uint8))
        return pil_img
          
    # Convert set of NumPy arrays to set of PIL images
    elif current_type == 'numpy_set':
        pil_images = []
        for img in images:
            pil_img = Image.fromarray(img.astype(np.uint8))
            pil_images.append(pil_img)
        return pil_images

    else:
        print("Attempted numpy_to_pil. Image type could not be identified -- data returned unmodified.")
        return images

def addNoise_gaussian(pil_image=None, mode='', alpha=.5, m=0, v=0.1):
    if pil_image is not None:
        width, height = pil_image.size
        base = np.array(pil_image) # Convert the PIL image to a numpy array
    else:
         # If no image provided, generate a 256x256 base image to use
        width = 256
        height = 256
        base = np.zeros((height, width)) # Create a blank grayscale image
    
    # Generate Gaussian noise
    mean = m
    variance = v
    sigma = np.sqrt(variance)
        
    if mode=='grayscale':
        gaussian = np.random.normal(mean, sigma, (height, width))
        # Scale the Gaussian noise to the range [0, 255]
        gaussian = np.interp(gaussian, (gaussian.min(), gaussian.max()), (0, 255)).astype(np.uint8)
        # Add the Gaussian noise to the image
        combined = (base*(1-alpha) + gaussian*alpha) #.astype(np.uint8)
                
    if mode=='RGB':
        #split by color channel
        red = np.random.normal(mean, sigma, (height, width))
        green = np.random.normal(mean, sigma, (height, width))
        blue = np.random.normal(mean, sigma, (height, width))
        # Stack the noise arrays to form an RGB image
        noise_stack = np.stack([red, green, blue], axis=-1)
        # Scale the noise to the range [0, 255]
        noise = np.interp(noise_stack, (noise_stack.min(), noise_stack.max()), (0, 255)).astype(np.uint8)
        combined = (alpha * noise + (1 - alpha) * base).astype(np.uint8)

    # Convert the numpy array to a PIL image
    outimage = numpy_to_pil(combined)

    # Display the image
    #outimage.show()
    
    return outimage


def addNoise_uniform(pil_image=None, alpha = .5, scale=1, m=0):
    if pil_image is not None:
        width, height = pil_image.size
        base = np.array(pil_image) # Convert the PIL image to a numpy array
    else:
        # Set image size
        width = 256
        height = 256
        base = np.full((height, width), 128, dtype=np.uint8) # Create a blank grayscale image
    mean = m
    
    noise = np.random.uniform(scale, size=(width, height))
    noise -= mean
    #noise *= np.sqrt(var / np.var(noise))
    combined = np.uint8(np.clip((alpha * noise + (1 - alpha) * base), 0, 255))
    
    # Convert the numpy array to a PIL image
    outimage = numpy_to_pil(combined)
   
    return outimage


def cdf_fast(image, normalize=True):
    image = pil_to_numpy(image).astype(np.uint8)

    # Calculate histogram of the image
    hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))

    # Calculate cumulative distribution
    cdf = np.cumsum(hist).astype(np.float64)
    if normalize:
        cdf = cdf / cdf[-1]

    return cdf