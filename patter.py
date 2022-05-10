import math
from PIL import Image
import io
from shitty_pillow import save_transparent_gif

# preload the pictures because i am a GOOD programmer who cares about performance
pat_frames = [
    Image.open("./img/pet0.gif").convert("RGBA"),
    Image.open("./img/pet1.gif").convert("RGBA"),
    Image.open("./img/pet2.gif").convert("RGBA"),
    Image.open("./img/pet3.gif").convert("RGBA"),
    Image.open("./img/pet4.gif").convert("RGBA"),
    Image.open("./img/pet5.gif").convert("RGBA"),
    Image.open("./img/pet6.gif").convert("RGBA"),
    Image.open("./img/pet7.gif").convert("RGBA"),
    Image.open("./img/pet8.gif").convert("RGBA"),
    Image.open("./img/pet9.gif").convert("RGBA")
]


#getPat takes a directory or a file-like stream
#returns a BytesIO stream
#format can be "webp" or "gif" (transparency is borked for gifs so be aware)
def getPat(avatar_file, format="webp"):
    avatar_x = 5
    avatar_y = 5
    avatar_width = 150
    avatar_height = 150
    image_width = 160
    image_height = 160
    hand_x = 0
    hand_y = 0
    delay = 20

    y_scale = [
        1,
        0.95,
        0.9,
        0.85,
        0.8,
        0.8,
        0.85,
        0.9,
        0.95,
        1
    ]

    x_scale = [
        0.80,
        0.85,
        0.90,
        0.95,
        1,
        1,
        0.95,
        0.90,
        0.85,
        0.80
    ]

    frames = []
    avatar_img = Image.open(avatar_file)
    for i in range(0, 10):
        avatar_actual_x = math.ceil((1 - x_scale[i]) * avatar_width / 2 + avatar_x)
        avatar_actual_y = math.ceil((1 - y_scale[i]) * avatar_height + avatar_y)
        avatar_actual_width = math.ceil(avatar_width * x_scale[i])
        avatar_actual_height = math.ceil(avatar_height * y_scale[i])

        scaled_avatar_img = avatar_img.resize((avatar_actual_width, avatar_actual_height))
        frame = Image.new(mode="RGBA", size=(image_width, image_height))
        frame.paste(scaled_avatar_img, (avatar_actual_x, avatar_actual_y))
        frame.paste(pat_frames[i], (hand_x, hand_y), pat_frames[i])
        frames.append(frame)
    

    output = io.BytesIO()
    if (format == "gif"):
        save_transparent_gif(frames, delay, output)
    else:    
        frames[0].save(output, format, 
            save_all = True,
            append_images = frames[1:],
            duration = delay,
            loop = 0
        )
    return output

if __name__ == "__main__":
    #getPat takes a path or a file-like stream
    #returns a BytesIO stream
    #output format can be "webp" or "gif" (transparency is borked for gifs so be aware)
    stream = getPat(open("./img/avatar.png", "rb"), "webp")
    #stream = getPat("./img/avatar.png", "webp")
    stream.seek(0)
    open("test.webp", "wb").write(stream.read())
