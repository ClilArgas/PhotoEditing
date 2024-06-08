Image Editing Program
Description
This is a command-line image editing program that allows you to apply various filters and adjustments to images.

Usage
To use the program, run the following command:

bash
Copy code
edit_image [options]
Available Filters and Options
Blur: Apply blur filter to the image.

--filter blur: Select the blur filter.
--x <value>: Horizontal blur strength.
--y <value>: Vertical blur strength.
Edge Detection: Apply edge detection filter to the image.

--filter edge_detection: Select the edge detection filter.
Sharpen: Apply sharpen filter to the image.

--filter sharpen: Select the sharpen filter.
--alpha <value>: Sharpening strength.
Saving the Photo
To save the edited photo, use the --save option followed by the desired file path.

Examples
bash
Copy code
# Apply blur filter with x=5 and y=5, then save the image
edit_image --filter blur --x 5 --y 5 --save output_blur.jpg

# Apply edge detection filter and save the image
edit_image --filter edge_detection --save output_edge.jpg

# Apply sharpen filter with alpha=1.5 and save the image
edit_image --filter sharpen --alpha 1.5 --save output_sharpen.jpg
