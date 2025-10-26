
PLATE_IMAGES = [
    # Flower plates
    {
        "color": "black",
        "symbol": "flower",
        "image": "flower_black.png"
    },
    {
        "color": "blue",
        "symbol": "flower",
        "image": "flower_blue.png"
    },
    {
        "color": "green",
        "symbol": "flower",
        "image": "flower_green.png"
    },
    {
        "color": "red",
        "symbol": "flower",
        "image": "flower_red.png"
    },
    {
        "color": "purple",
        "symbol": "flower",
        "image": "flower_purple.png"
    },
    {
        "color": "cyan",
        "symbol": "flower",
        "image": "flower_cyan.png"
    },
    # Bird plates
    {
        "color": "blue",
        "symbol": "bird",
        "image": "bird_blue.png"
    },
    {
        "color": "red",
        "symbol": "bird",
        "image": "bird_red.png"
    },
    {
        "color": "green",
        "symbol": "bird",
        "image": "bird_green.png"
    },
    {
        "color": "black",
        "symbol": "bird",
        "image": "bird_black.png"
    },
    {
        "color": "purple",
        "symbol": "bird",
        "image": "bird_purple.png"
    },
    {
        "color": "cyan",
        "symbol": "bird",
        "image": "bird_cyan.png"
    },

    # Fish plates
    {
        "color": "blue",
        "symbol": "fish",
        "image": "fish_blue.png"
    },
    {
        "color": "red",
        "symbol": "fish",
        "image": "fish_red.png"
    },
    {
        "color": "green",
        "symbol": "fish",
        "image": "fish_green.png"
    },
    {
        "color": "black",
        "symbol": "fish",
        "image": "fish_black.png"
    },
    {
        "color": "purple",
        "symbol": "fish",
        "image": "fish_purple.png"
    },
    {
        "color": "cyan",
        "symbol": "fish",
        "image": "fish_cyan.png"
    }
]

# define the price of each colored plate (per eighth of a plate)
COLOR_PRICES = {
    "blue": 1,
    "black": 2,
    "green": 4,
    "red": 8,
}

COLOR_ORDER = ["blue", "black", "green", "red"]


def calculate_price_of_plate(plate) -> int:
    price = 0
    for color_of_eighth in plate.fragment_colors:
        price += COLOR_PRICES[color_of_eighth] # TypeError: unhashable type: 'list'
    
    # bonus?
    if len(set(plate.fragment_colors)) == 1:
        # only one color -> bonus
        price *= 2
    if len(set(plate.fragment_symbols)) == 1:
        # only one symbol -> bonus
        price *= 2
    return price