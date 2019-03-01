from dataclasses import dataclass
from itertools import tee


@dataclass
class Photo:
    _id: int
    vertical: bool
    tags: set


def parse_photos(filename):
    with open(filename, 'r') as file:
        data = []
        num = 0
        for line in file:
            if line[0] not in ['H', 'V']:
                continue
            raw_photo = line.split(' ')
            raw_photo[-1] = raw_photo[-1][:-1]  # remove \n
            data.append(Photo(num, raw_photo[0] == 'V', set(raw_photo[2:])))
            num += 1
        return data


def parse_slides(filename):
    slides = []
    with open(filename, 'r') as res_file:
        next(res_file)
        for line in res_file:
            slides.append(list(map(int, line.split(' '))))
    return slides


def save_slides(slides, filename):
    with open(filename, 'w') as file:
        file.write(str(len(slides)) + '\n')
        for slide in slides:
            file.write(' '.join(map(str, slide)) + '\n')


def get_pair_interest(tags1, tags2):
    return min(map(len, (tags1 - tags2, tags2 - tags1, tags1 & tags2)))


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_slideshow_interest(photos, slides):
    slideshow_tags = []
    for slide in slides:
        tags = set()
        for photo_index in slide:
            try:
                photo = photos[photo_index]
            except IndexError:
                print(photo_index)
                raise
            if len(slide) == 2 and not photo.vertical:
                raise RuntimeError
            tags |= photo.tags
        slideshow_tags.append(tags)

    tags_pairs = pairwise(slideshow_tags)

    sum = 0
    for tags_pair in tags_pairs:
        sum += get_pair_interest(*tags_pair)
    return sum
