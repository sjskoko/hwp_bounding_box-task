import argparse
from dartplumber import Extractor
from util import *

def main(args):

    pdf_extractor = Extractor(args)
    image_result = pdf_extractor.create_bbox_with_img_save()

    return image_result

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Argparse Tutorial')

    parser.add_argument('--table', '-t', action='store_true', default=False)
    parser.add_argument('--image', '-i', action='store_true', default=False)
    parser.add_argument('--caption', '-c', action='store_true', default=False)

    parser.add_argument('--pdf_dir', '-dir', type=str, default='input')
    parser.add_argument('--save_dir', '-save', type=str, default='output')

    parser.add_argument('--crop', '-crop', action='store_true', default=False)
    parser.add_argument('--page_image', '-page', action='store_true', default=False)


    args = parser.parse_args()

    main(args)
