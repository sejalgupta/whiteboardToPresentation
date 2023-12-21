class PresentationTheme:
    def __init__(self, prompt_answer):
        self.background_color = prompt_answer["background_color"]

        self.title_style = {}
        self.body_style = {} 
        for key in ["font", "size", "color"]:
            try:
                self.title_style[key] = prompt_answer["title"][key]
            except:
                self.title_style[key] = None
            
            try:
                self.body_style[key] = prompt_answer["body"][key]
            except:
                self.body_style[key] = None

    def update_background_color(self, new_color):
        self.background_color = new_color

    def update_title_style(self, new_color=None, new_size=None, new_font=None):
        if new_color is not None:
            self.title_style['color'] = new_color
        if new_size is not None:
            self.title_style['size'] = new_size
        if new_font is not None:
            self.title_style['font'] = new_font

    def update_body_style(self, new_color=None, new_size=None, new_font=None):
        if new_color is not None:
            self.body_style['color'] = new_color
        if new_size is not None:
            self.body_style['size'] = new_size
        if new_font is not None:
            self.body_style['font'] = new_font

    def get_theme_info(self):
        return {
            'background_color': self.background_color,
            'title': self.title_style,
            'body': self.body_style
        }