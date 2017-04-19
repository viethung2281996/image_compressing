from PIL import Image
import random


def _encodeImage4bit(imagePixels, width, height):
    encodedImage = bytearray()

    count = 0

    prev = imagePixels[0]
    tempmap = ""

    for pixel in imagePixels:
        if count >= 15:
            encodedImage.append(15)
            encodedImage.append(prev)
            tempmap += "1"
            tempmap += "0"
            count = 0
            prev = pixel

        if pixel == prev:
            count += 1
        else:
            if count > 1:
                encodedImage.append(count)
                tempmap += "1"
            encodedImage.append(prev)
            tempmap += "0"
            count = 1
            prev = pixel

    if count > 1:
        encodedImage.append(count)
        tempmap += "1"

    encodedImage.append(prev)
    tempmap += "0"

    encodedImage.extend([0] * _remaining(len(encodedImage)))
    tempmap += "1"*_remaining(len(tempmap))

    encodedImage = _set4bitMap(tempmap, encodedImage)

    return encodedImage


def _set4bitMap(imgMap, encodedImage):
    newImgMap = _divideByRow(imgMap, 8)

    tempImg = [_merge4bitTo8bit(encodedImage[i], encodedImage[i + 1]) for i in range(0, len(encodedImage), 2)]
    tempImg = _divideByRow(list(tempImg), 4)

    return bytearray(_flattenListOfList(_mergeMap(tempImg, newImgMap)))


def _decodeImage4bit(encodedImage, width, height):
    decodedImage = []

    imgMap, encImg = _get4bitMap(encodedImage)

    for index, i in enumerate(imgMap):
        if i == '1' and encImg[index] == 0:
            break

        if i == '1':
            decodedImage.extend([encImg[index + 1]] * encImg[index])
        elif imgMap[index - 1] != '1' or index == 0:
            decodedImage.append(encImg[index])

    return decodedImage


def _get4bitMap(encodedImage):
    imgMap = ""

    newEncodedImage = list(encodedImage)

    I = range(0, len(newEncodedImage), 5)

    for i in I:
        imgMap += '{0:08b}'.format(newEncodedImage[i])

    for i in sorted(list(I), reverse = True):
        del newEncodedImage[i]

    newEncodedImage = _flattenListOfList([_split8bitTo4bit(i) for i in newEncodedImage])

    return (imgMap, newEncodedImage)


def _split8bitTo4bit(eightbit):
    leftmask = 240
    rightmask = 15
    left = (eightbit & leftmask) >> 4
    right = eightbit & rightmask
    return (left, right)


def _merge4bitTo8bit(left, right):
    return (left << 4) | right


_remaining = lambda x, y = 8: 0 if x % y == 0 else y - (x % y)
_mergeMap = lambda z, x:[[int(x[index], 2)] + i for index, i in enumerate(z)]
_flattenListOfList = lambda flat:[item for sublist in flat for item in sublist]
_divideByRow = lambda flat, size: [flat[i:i + size] for i in range(0, len(flat), size)]


if __name__ == "__main__":
    img = [15] * 100
    img.extend([random.randrange(0, 16) for n in range(300)])
    encImg = _encodeImage4bit(img, 20, 20)
    decImg = _decodeImage4bit(encImg, 20, 20)
    print(str(decImg == img))

    imgpath = "/home/thang/Pictures/a.png"
    img2 = Image.open(imgpath)
    encImg2 = _encodeImage4bit(list(img2.getdata(0)), img2.size[0], img2.size[1])
    decImg2 = _decodeImage4bit(encImg2, img2.size[0], img2.size[1])
    print(str(decImg2 == list(img2.getdata(0))))