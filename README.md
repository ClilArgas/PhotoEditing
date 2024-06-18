#Image Editing Software
##Description
first command : edit_image --image <image_path>

filters: --filter <filter_name> : {blur- params: --x <x_val> --y <y_val> , edge_detection - params: none, sharpen- params: --alpha <alpha>}
adjustments: --adjust <adjust_name> <level> :{brightness, contrast, saturation}

quit for quiting and if u want to save ur photo use --save <path> to save it 

example of usage: edit_image --image <path_to_image> --filter blur  --x 5 --y 5 --adjust contrast 1.5 --filter sharpen --alpha 0.05 --save <path_to_save>

@clilArgas
