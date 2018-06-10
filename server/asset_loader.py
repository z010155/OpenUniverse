import os
from typing import Tuple, List


class AssetLoader:
    @staticmethod
    def load_names() -> Tuple[List[str], List[str], List[str]]:
        pth1 = os.path.join(os.path.realpath(''), 'assets', 'names', 'first.txt')
        pth2 = os.path.join(os.path.realpath(''), 'assets', 'names', 'middle.txt')
        pth3 = os.path.join(os.path.realpath(''), 'assets', 'names', 'last.txt')

        with open(pth1, 'r') as f:
            first = f.readlines()

        with open(pth2, 'r') as f:
            middle = f.readlines()

        with open(pth3, 'r') as f:
            last = f.readlines()

        return first, middle, last
