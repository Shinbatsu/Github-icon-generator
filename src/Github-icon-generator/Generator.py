from PIL import ImageDraw, Image
import hashlib
import re


class Icon:
    BACKGROUND_COLOR = '#f2f2f2'

    def __init__(self, form: bin, color: hex = '#000000', icon_size: int = 12):
        self.icon_size = icon_size
        self.form = form
        self.color = color
        self.IMAGE_SIZE = icon_size ** 2
        self.icon = Image.new('RGB', (self.IMAGE_SIZE, self.IMAGE_SIZE), self.BACKGROUND_COLOR)
        self.brush = ImageDraw.Draw(self.icon)

    def generate_icon(self):
        matrix = re.findall(r'.{' + f'{self.icon_size // 2 - 1}' + '}', self.form)
        # TODO optimize! 🍕 🍕 🍕 🍕
        for i in range(self.icon_size, self.IMAGE_SIZE - self.icon_size, self.icon_size):
            for j in range(self.icon_size, len(matrix[0]) * self.icon_size + self.icon_size, self.icon_size):
                if matrix[i // self.icon_size - 1][j // self.icon_size - 1] == '1':
                    for x in range(self.icon_size + 1):
                        for y in range(self.icon_size + 1):
                            self.brush.point((i + x, j + y), self.color)
                            self.brush.point((i - x + self.icon_size, self.IMAGE_SIZE - j - y), self.color)
        self.icon = self.icon.rotate(-90)
        self.icon.show()


class UserHash:
    def __init__(self, userName: str, size: int = 12):
        self.__user_hash = hashlib.sha3_512(userName.encode('utf8')).hexdigest()
        self.size = size

    def get_binary_hash(self) -> bin:
        if self.size < 4 or self.size > 32 or self.size % 2:
            raise "Incorrect size"
        return bin(int(self.__user_hash, 16))[2:(self.size - 2) ** 2 // 2 + 2]

    def get_rgb_color(self):
        return '#' + ''.join(
            [('0' + (hex(int(self.__user_hash[i * 2:i * 2 + 2], 16) % 230)[2:]))[-2:] for i in range(3)])


class Avatar:
    def __init__(self, userName, size=12):
        self.__hash = UserHash(userName, size)
        self.size = size

    def get_icon(self):
        self.user_icon = Icon(self.__hash.get_binary_hash(), self.__hash.get_rgb_color(), self.size)
        return self.user_icon.generate_icon()


if __name__ == '__main__':  # icon size should be even and in range [4...32]; for size 32, icon will be 1024x1024 (32**2)
    print(Avatar('Shinbatsu').get_icon())
    print(Avatar('Shuusa').get_icon())
    print(Avatar('qwerty').get_icon())
    print(Avatar('pizza...').get_icon())
