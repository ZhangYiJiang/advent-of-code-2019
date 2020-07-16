BLACK = 0
WHITE = 1
TRANSPARENT = 2


def get_layers(pixels, width, height):
    layers = []
    size = width * height
    for start in range(0, len(pixels), size):
        layers.append(list(map(int, pixels[start:start+size])))
    return layers


def calculate_checksum(layers):
    with_most_zeros = min(layers, key=lambda layer: layer.count(0))
    return with_most_zeros.count(1) * with_most_zeros.count(2)


def calculate_image(layers, width, height):
    final_iamge = []
    for p in range(width * height):
        for layer in layers:
            if layer[p] == BLACK:
                final_iamge.append(' ')
                break
            elif layer[p] == WHITE:
                final_iamge.append('X')
                break
    return final_iamge

if __name__ == "__main__":
    WIDTH = 25
    HEIGHT = 6

    with open('../input/day_8.in') as f:
        pixels = f.readline()
    
    layers = get_layers(pixels, WIDTH, HEIGHT)
    image = calculate_image(layers, WIDTH, HEIGHT)
    for c in range(HEIGHT):
        print(''.join(image[c * WIDTH : (c+1) * WIDTH]))

