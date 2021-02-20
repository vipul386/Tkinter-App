from PIL import Image, ImageDraw


class my_button:
    def btn(size, padding=0, fill="white"):
        width, height = size
        img = Image.new("RGBA", (width, height), "white")
        img.putalpha(0)
        draw = ImageDraw.Draw(img, "RGBA")
        draw.rectangle((padding, padding, width - padding, height - padding),
                       fill)
        img.show()

    def o_btn(size, padding=0, fill="white"):
        width, height = size
        img = Image.new("RGBA", (width, height), "white")
        img.putalpha(0)
        draw = ImageDraw.Draw(img, "RGBA")
        draw.ellipse((padding, padding, width - padding, height - padding),
                     fill)
        img.show()

    def round_btn(size, radius, padding=0, fill="green"):
        width, height = size
        img = Image.new("RGBA", (width, height), "white")
        img.putalpha(0)
        draw = round_rectangle(size=(width - padding, height - padding),
                               radius=radius, fill=fill)
        img.paste(draw, (int(padding / 2), int(padding / 2)))
        img.show()


def round_rectangle(size, radius, fill):
    width, height = size
    rectangle = Image.new('RGBA', size, fill)

    corner = Image.new('RGB', (radius, radius), (0, 0, 0, 0))
    corner.putalpha(0)
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)

    rectangle.paste(corner, (0, 0))
    rectangle.paste(corner.rotate(90), (0, height - radius))
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))

    return rectangle
