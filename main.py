import disnake
import json
import logging
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PING_COMMAND = "!ping"
CAPTION_COMMAND = "!c"
CAT_LOCATION = "cat.jpeg"

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%I:%M:%S',
    level=logging.INFO
)

with open('config.json') as f:
    config = json.load(f)

client = disnake.Client()

@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    logging.info(f'Recieved message from {message.author}: \"{message.content}\"')

    if message.author == client.user:
        return

    if message.content.startswith(PING_COMMAND):
        await message.channel.send(file=disnake.File(CAT_LOCATION))
    elif message.content.startswith(CAPTION_COMMAND):
        caption_image(
            fetch_cat_image(),
            message.content[len(CAPTION_COMMAND):]
        ).convert("RGB").save(CAT_LOCATION)
        await message.channel.send(file=disnake.File(CAT_LOCATION))

def caption_image(img, label):
    draw = ImageDraw.Draw(img)
    fontsize = text_size(label, img.size)
    borderwidth = round((1/30)*fontsize)
    color = '#fff'
    bordercolor = '#000'
    font = ImageFont.truetype("fonts/impact.ttf", fontsize)
    position = text_position(label, img.size, font)

    draw.text(position, label, font=font, fill=color, stroke_fill=bordercolor, stroke_width=borderwidth)
    return img

def text_position(text, imgsize, font):
    xi, yi = imgsize
    xt, yt = font.getsize(text)
    x = (xi - xt) / 2
    logging.info(f'xi: {xi}, xt: {xt}, x: {x}')
    return x, .85*yi

def text_size(text, imgsize):
    _, y = imgsize
    return round(.08*y)

def fetch_cat_image():
    response = requests.get('https://api.thecatapi.com/v1/images/search', headers = {"x-api-key": config["CAT_API_TOKEN"]})
    url = response.json()[0]["url"]
    img = Image.open(BytesIO(requests.get(url).content))
    logging.info(f'Recieved response {response}, extracted url {url} and fetched image {img}')
    return img


if __name__ == '__main__':
    client.run(config['DC_TOKEN'])
