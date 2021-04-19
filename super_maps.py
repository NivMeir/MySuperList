from PIL import Image, ImageDraw

class Maps:

    def __init__(self):
        self.__arrows = {'A1' : ((350, 575),(380, 605)),
                         'B1': ((350, 515), (380, 545)),
                         'C1': ((350, 455), (380, 485)),
                         'A2': ((350, 365), (380, 395)),
                         'B2': ((350, 305), (380, 335)),
                         'C2': ((350, 245), (380, 275)),
                         'D2': ((350, 185), (380, 215)),
                         'A3': ((350, 100), (380, 130)),
                         'B3': ((350, 40), (380, 70)),
                         'A4': ((990, 100), (1020, 130)),
                         'A5': ((845, 215), (875, 245)),
                         'B5': ((845, 285), (875, 315)),
                         'C5': ((845, 355), (875, 385)),
                         'A6': ((960, 255), (990, 285)),
                         'B6': ((960, 340), (990, 370)),
        }


    def make_a_copy(self, filename):
        from shutil import copyfile
        src = r'D:\CYBER\Super List project\static\map.jpg'
        dst = r'D:\CYBER\Super List project\static\user_maps'
        dst +=  str(filename)
        print(dst)
        copyfile(src, dst)

    def delete_last_copy(self, filename):
        import glob
        import os
        try:
            firstletter = filename[1]
            path = r'static\user_maps'
            path += "\\" + str(firstletter) + "*"
            arr = glob.glob(path)
            for url in arr:
                os.remove(url)
        except BaseException as e:
            print(e)


    def draw_arrows(self, mylist, filename):
        self.delete_last_copy(filename)
        self.make_a_copy(filename)
        path = r'D:\CYBER\Super List project\static\user_maps'
        path += filename
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        for product in mylist:
            place = str(product['shelf']) + str(product['pclass'])
            west_north = self.__arrows[place][0]
            east_south = self.__arrows[place][1]
            color = (6, 253, 39)
            draw.ellipse([west_north, east_south],fill=color, outline=color)
        im.save(path)

