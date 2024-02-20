from PIL import Image
from PIL import features
import glaxnimate


def png_gif_prepare(image):
    """
    Converts the frame image from RGB to indexed, preserving transparency
    """
    if image.mode not in ["RGBA", "RGBa"]:
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    image = image.convert("RGB").convert('P', palette=Image.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    image.paste(255, mask=mask)
    return image


def save_gif(document, file, skip_frames=1):
    start = int(document.main.animation.first_frame)
    end = int(document.main.animation.last_frame)

    # Get all frames as PIL images
    frames = []
    for i in range(start, end+1, skip_frames):
        frames.append(png_gif_prepare(document.render_image(i)))

    # Save as animation
    duration = int(round(1000 / document.main.fps * skip_frames / 10)) * 10
    frames[0].save(
        file,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0,
        transparency=255,
        disposal=2,
    )

# Initialize environment
with glaxnimate.environment.Headless():

    document = glaxnimate.model.Document("")

    # Load the lottie JSON
    with open("out.svg", "rb") as input_file:
        glaxnimate.io.registry.from_extension("svg").load(document, input_file.read())

    # Save as GIF
    with open("MyFile.gif", "rb") as output_file:
        save_gif(document, output_file)