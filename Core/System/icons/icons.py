from PIL import Image, ImageDraw

def create_start_icons():
    file_explorer_icon = Image.new('RGB', (50, 50), color='blue')
    draw = ImageDraw.Draw(file_explorer_icon)
    draw.text((15, 15), "FE", fill='white')
    file_explorer_icon.save("start_file_explorer_icon.png")

    nanodraft_icon = Image.new('RGB', (50, 50), color='green')
    draw = ImageDraw.Draw(nanodraft_icon)
    draw.text((10, 15), "ND", fill='white')
    nanodraft_icon.save("start_nanodraft_icon.png")

create_start_icons()
