from PIL import Image

def scale_image(img_path, target_width, target_height):
    
    img_width, img_height = None, None
    
    with Image.open(img_path) as img:
        img_width = img.width
        img_height = img.height

    img_aspect = img_width / img_height
    target_aspect = target_width / target_height

    if img_aspect > target_aspect:
        scale_factor = target_width / img.width
    else:
        scale_factor = target_height / img.height
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)

    return new_width, new_height
