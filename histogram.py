import cv2
import matplotlib.pyplot as plt
import os


def get_histogram_all(path):
    '''
    Returns the histogram of all images in a folder.
    '''
    hist = []
    names = []
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            name_main = filename.split('_')[-1][:-4]
            img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)
            hist.append(cv2.calcHist([img], [0], None, [256], [0, 256]))
            names.append(name_main)
    return hist, names

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.realpath(__file__))
    input_folder = os.path.join(project_dir, "sample_images_noisy_gaussian")
    # input_folder = os.path.join(project_dir, "sample_images_processed")
    # input_folder = os.path.join(project_dir, "sample_images_noisy_uniform")

    hist, names = get_histogram_all(input_folder)
    print(names)
    # set y axis limit to 1000 
    # plt.ylim(0, 2000)
    # for h in hist:
    #     plt.plot(h)
    # plt.show()