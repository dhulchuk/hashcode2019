import itertools
import random

from tools import parse_photos, parse_slides, get_slideshow_interest, save_slides

filenames = [
    'a_example.txt',
    'b_lovely_landscapes.txt',  # 80000
    'c_memorable_moments.txt',  # 10000
    'd_pet_pictures.txt',
    'e_shiny_selfies.txt',
]


def random_v_solution(data):
    res = []
    used = set()
    for i, photo in enumerate(data[:-1]):
        if i in used:
            continue
        if len(used) == len(data):
            break
        used.add(i)
        if photo.vertical:
            pair = i
            while pair == i or pair in used:
                pair = random.randint(i, len(data)-1)
            used.add(pair)
            res.append((i, pair))
    return res


def random_hv_solution(data):
    res = []
    used = set()
    for i, photo in enumerate(data[:-1]):
        if i in used:
            continue
        if len(used) == len(data):
            break
        used.add(i)
        if photo.vertical:
            pair = i
            while pair == i or pair in used or not data[pair].vertical:
                pair = random.randint(i, len(data)-1)
            used.add(pair)
            res.append((i, pair))
        else:
            continue
            res.append((i,))
    return res


def rotate_two(slides, i):
    slides[i], slides[i+1] = slides[i+1], slides[i]


def main():
    data = parse_photos(filenames[4])
    m = 0
    # res_slides = []
    slides = random_hv_solution(data)
    try:
        for x in range(1000):
            i = random.randint(0, len(slides) - 2)
            rotate_two(slides, i)
            # random.shuffle(slides)
            result = get_slideshow_interest(data, slides)
            if result > m:
                print(f'good: {result}')
                m = result
            else:
                print(f'bad: {result}')
                rotate_two(slides, i)
    except KeyboardInterrupt:
        print(f'res: {m}')
        save_slides(slides, 'output.txt')
        # slides = parse_slides('combined_c.txt')
        # random.shuffle(slides)
        # print(get_slideshow_interest(data, slides))
    else:
        print(f'res: {m}')
        save_slides(slides, 'output.txt')



if __name__ == '__main__':
    main()
