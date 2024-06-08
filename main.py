from PIL import Image
import numpy as np
import threading
import time
from Adjustments.contrast import Contrast
from Adjustments.saturation import Saturation
from Adjustments.brightness import Brightness
from Filters.blur import Blur
from Filters.sharpen import Sharpen
from Filters.edge_detection import EdgeDetection

# Maps for filters and adjustments
filters = {
    "blur": Blur,
    "sharpen": Sharpen,
    "edge_detection": EdgeDetection
}
adjustments = {
    "brightness": Brightness,
    "saturation": Saturation,
    "contrast": Contrast
}


# Define the image processing function
def process_image(image_array, adjs_and_fils, show, save_addr):
    # Apply each filter/adjustment to the photo
    for adjust_filter in adjs_and_fils:
        image_array = adjust_filter.apply(image_array)
    # Convert the image back to an image format
    image = Image.fromarray(image_array.astype(np.uint8))
    # Save or show the image
    if show:
        image.show(title="Edited Image")
    else:
        image.save(save_addr)


# at first made this function to be run by a single thread but at the end changed it to multi-threaded
def cmd_line_interpreter():
    # Running the CMD until a quit command is called or an error will occur
    while True:
        # 1 parse the cmd lines from keyboard
        # 2 get the image from the url and if not exists print an error message
        # 3 create the requested filters or adjustments from the cmd and check parameters
        image_array, adjs_and_fils, show, save_addr, q = parse_input()
        # 4 realize whether to stop the program
        if q:
            break
        # 5 create a thread to process the image
        processing_thread = threading.Thread(target=process_image, args=(image_array, adjs_and_fils, show, save_addr))
        processing_thread.start()
        # continue to accept and parse commands in the main thread
        # simulating command line processing delay
        time.sleep(0.5)


def parse_input():
    line = input("Provide here the photo u want to edit with the editing details, quit for exiting:\n")
    parsed_input = line.split()
    image_matrix = adjustments_and_filters = []
    show = True
    save_address = ''
    q = False
    if parsed_input[0] == 'quit':
        q = True
    # initiate vars
    else:
        i = 1
        # iterating through the command to parse the data
        while i < len(parsed_input):
            # converting the image to a matrix
            # need to handle wrong url
            if parsed_input[i] == '--image':
                try:
                    image_path = parsed_input[i+1]
                    image_matrix = convert_image_to_matrix(image_path)
                    i += 2
                except Exception as e:
                    print(f"An error happened during uploading the image: {e}")
                    q = True
                    break
            # adding an adjustment to the array to create an adjustment object later
            elif parsed_input[i] == '--adjust':
                # building an adjustment object according to the level and the type
                adjustment_type = parsed_input[i+1]
                level = float(parsed_input[i+2])
                adjustments_and_filters.append(build_an_adjustment(adjustment_type,level))
                i += 3
            # adding a filter to the array to create an adjustment object later
            elif parsed_input[i] == '--filter':
                filter_type = parsed_input[i+1]
                params = {}
                if filter_type == 'blur':
                    # getting the values of the x and y
                    x_kernel = int(parsed_input[i+3])
                    y_kernel = int(parsed_input[i+5])
                    if parsed_input[i+2] == '--y':
                        x_kernel, y_kernel = y_kernel, x_kernel
                    params = {
                        "x": x_kernel,
                        "y": y_kernel
                    }
                    i += 6
                if filter_type == 'sharpen':
                    # getting alpha
                    params = {
                        "alpha": float(parsed_input[i+3])
                    }
                    i += 4
                if filter_type == 'edge_detection':
                    i += 2
                adjustments_and_filters.append(build_a_filter(filter_type, params))
            elif parsed_input[i] == '--save':
                show = False
                save_address = parsed_input[i+1]
                i += 2
            else:
                print("Unknown command please verify your input and try again")
                q = True
                break
    return [image_matrix, adjustments_and_filters, show, save_address, q]


# checked online how to convert an image to a numpy array
def convert_image_to_matrix(url):
    image = Image.open(url)
    return np.array(image)


def build_an_adjustment(adjustment_type, level):
    return adjustments.get(adjustment_type)(level)


def build_a_filter(filter_type, params):
    return filters.get(filter_type)(params)


if __name__ == '__main__':
    cmd_line_interpreter()



