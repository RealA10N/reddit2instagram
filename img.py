from PIL import Image, ImageFont, ImageDraw
import typing


class Title:

    def __init__(self,
                 icon_mask: Image.Image,
                 left_text: str = None,
                 right_text: str = None,
                 ):
        self.icon_mask = icon_mask
        self.left_text = left_text
        self.right_text = right_text

    def generate(self,
                 color: typing.Union[str,
                                     typing.Tuple[int, int, int]] = "black",
                 font: ImageFont.FreeTypeFont = None,
                 icon_padding: int = 25,
                 icon_size: typing.Union[int, typing.Tuple[int, int]] = None,
                 ):

        # Resize icon mask if needed
        icon_mask = self.icon_mask
        if icon_size is not None:
            if isinstance(icon_size, int):
                icon_size = (icon_size, icon_size)
            icon_mask = icon_mask.resize(icon_size)

        # Creating a new canvas, size is not yet decided (:
        canvas = Image.new(mode="RGBA", color=(255, 255, 255, 0), size=(1, 1))
        draw = ImageDraw.Draw(canvas)

        sizes = [
            draw.textsize(text, font=font)
            for text in [self.left_text, self.right_text]
            if text is not None
        ] + [icon_mask.size]

        canvas_height = max(size[1] for size in sizes)
        canvas_width = sum(size[0] for size in sizes) + \
            ((len(sizes) - 1) * icon_padding)

        canvas = canvas.resize((canvas_width, canvas_height))
        draw = ImageDraw.Draw(canvas)

        x = 0
        mid_y = int(canvas_height / 2)

        # Add left text
        if self.left_text is not None:
            draw.text((x, mid_y), self.left_text,
                      fill=color, font=font, anchor="lm")
            x += draw.textsize(self.left_text, font=font)[0] + icon_padding

        # Add icon
        icon_y = int((canvas_height - icon_mask.height) / 2)
        icon_color = Image.new(
            mode="RGB", size=icon_mask.size, color=color)
        canvas.paste(icon_color, box=(x, icon_y), mask=icon_mask)
        x += icon_mask.width + icon_padding

        # Add right text
        if self.right_text is not None:
            draw.text((x, mid_y), self.right_text,
                      fill=color, font=font, anchor="lm")

        return canvas


class TitleCollection:

    def __init__(self):
        self.__titles = list()

    @property
    def titles(self):
        return self.__titles

    def create(self, *args, **kwargs):
        """ Create and add a title to the collection. """

        title = Title(*args, **kwargs)
        self.add(title)

    def add(self, title: Title):
        """ Add an exsiting title to the collection. """

        if not isinstance(title, Title):
            raise TypeError("Can't add non title object")
        self.__titles.append(title)

    @staticmethod
    def __paste_on_canvas(canvas, img, x=None, y=None):

        if x is None:
            x = int((canvas.width - img.width) / 2)

        if y is None:
            y = int((canvas.height - img.height) / 2)

        canvas.paste(img, box=(x, y))

    def generate(self,
                 order_type: str,
                 titles_padding: int = 0,
                 **kwargs
                 ):

        if order_type.lower() == "col":
            def size_in_dir(img): return img.height
            def size_not_dir(img): return img.width
            def gen_canvas_size(in_dir, not_dir): return (not_dir, in_dir)
            def convert_pos_to_kwarg(position): return {"y": position}

        elif order_type.lower() == "row":
            def size_in_dir(img): return img.width
            def size_not_dir(img): return img.height
            def gen_canvas_size(in_dir, not_dir): return (in_dir, not_dir)
            def convert_pos_to_kwarg(position): return {"x": position}

        else:
            raise ValueError("Order type must be 'COL' or 'ROW'.")

        # Generate titles
        title_imgs = [title.generate(**kwargs) for title in self.titles]

        # Calculate canvas size
        canvas_size_in_dir = sum(size_in_dir(img)
                                 for img in title_imgs) + \
            (titles_padding * (len(title_imgs) - 1))
        canvas_size_not_dir = max(size_not_dir(img) for img in title_imgs)

        # Create canvas
        canvas_size = gen_canvas_size(canvas_size_in_dir, canvas_size_not_dir)
        canvas = Image.new(mode="RGBA", size=canvas_size,
                           color=(255, 255, 255, 0))

        # Add titles to canvas
        cur_pos_in_dir = 0
        for title in title_imgs:
            kwarg = convert_pos_to_kwarg(cur_pos_in_dir)
            self.__paste_on_canvas(canvas, title, **kwarg)
            cur_pos_in_dir += size_in_dir(title) + titles_padding

        return canvas

    def generate_row(self, *args, **kwargs):
        return self.generate(order_type="row", *args, **kwargs)

    def generate_col(self, *args, **kwargs):
        return self.generate(order_type="col", *args, **kwargs)


class Post:

    def __init__(self,
                 img: Image.Image,
                 ):
        # Save the given base image.
        self.__img = img

    @property
    def img(self,):
        """ Returns the pillow image, given in the constructor. """
        return self.__img

    def generate(self,
                 size: typing.Union[int, typing.Tuple[int, int]] = (1000, 1080),
                 padding: typing.Union[int, typing.Tuple[int, int]] = 40,
                 background_color: typing.Union[str,
                                                typing.Tuple[int, int, int]] = "white",
                 titles: TitleCollection = None,
                 **kwargs
                 ):

        # Convert single ints to tuples
        if isinstance(size, int):
            size = (size, size)

        if isinstance(padding, int):
            padding = (padding, padding)

        base_img = Image.new(
            mode="RGB", color=background_color, size=size)
        width, height = [size - (cur_pad * 2)
                         for size, cur_pad in zip(size, padding)]
        img_ratio = self.img.size[0] / self.img.size[1]

        if img_ratio >= 1:
            # if horizontal
            # width is already calculated.
            # will calculate the height depending on the ratio and calculated width.
            height = int(width / img_ratio)

        else:
            # if vertical
            # height is already calculated.
            # will calculate the width depending on the ratio and calculated height.
            width = int(height * img_ratio)

        img_size = (width, height)
        img = self.img.resize(img_size)

        # paste image in the middle of the base image
        paste_location = [
            int((cur_final_img_size - cur_img_size) / 2)
            for cur_img_size, cur_final_img_size
            in zip(img_size, size)
        ]
        base_img.paste(img, box=paste_location)

        if titles is not None:
            self._add_titles(base_img, titles, **kwargs)

        return base_img

    @staticmethod
    def _add_titles(img: Image.Image,
                    titles: TitleCollection,
                    titles_size: int = None,
                    titles_y_offset: int = 0,
                    ** kwargs,):
        """ Add a title collection row to the image. """

        titles_img = titles.generate_row(**kwargs)

        if titles_size is not None:
            # resize so `titles_size` is the height
            ratio = titles_img.height / titles_size
            new_width = int(titles_img.width / ratio)
            new_height = titles_size
            titles_img = titles_img.resize((new_width, new_height))

        paste_x = int((img.width - titles_img.width) / 2)
        paste_y = img.height - int((titles_img.height / 2)) - titles_y_offset
        img.paste(titles_img, box=(paste_x, paste_y), mask=titles_img)
