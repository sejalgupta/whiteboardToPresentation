from pptx import Presentation
from constants import layout_mapping
import json
from helper_functions import scale_image

def add_slide(presentation, information):
    """
    Add a slide to the presentation with flexible content handling.

    Parameters
    - presentation (Presentation obj): the main presentation that is being modified
    - information (dictionary): the layout of the slide and data being placed on the slide including the titles, subtitles, content, and more
    """

    layout = layout_mapping[information["layout"]]
    slide_layout = presentation.slide_layouts[layout.value]
    slide = presentation.slides.add_slide(slide_layout)

    for placeholder in slide.placeholders:
        
        # ADD SUBTITLE
        if 'subtitle' in placeholder.name.lower() or "text" in placeholder.name.lower():
            title = information["subtitle"].pop(0)
            placeholder.text = title
        
        # ADD TITLE
        elif 'title' in placeholder.name.lower():
            title = information["title"].pop(0)
            placeholder.text = title

        # ADD PICTURE / ICON
        elif 'picture' in placeholder.name.lower():
            img_path = information["picture"].pop(0)
            placeholder.insert_picture(img_path)

        # ADD IMAGE OR TEXT IN CONTENT HOLDER
        elif 'content' in placeholder.name.lower():
            content_dict = information["content"].pop(0)
            if content_dict["type"] == "text":
                tf = placeholder.text_frame
                tf.text = content_dict["text"]
            else:
                img_path = content_dict["image"]
                image_width, image_height = scale_image(img_path, placeholder.width, placeholder.height)

                # add image as a shape
                slide.shapes.add_picture(img_path, placeholder.left, placeholder.top, image_width, image_height)

def main():
    name = "example_presentation"
    

    pres = Presentation()

    #load slides content
    slides_content = json.load(open(f"{name}.json"))

    #add each slide
    for slide in slides_content:
        add_slide(pres, slide)

    pres.save(f'{name}.pptx')
    print("Presentation created successfully!")

if __name__ == "__main__":
    main()