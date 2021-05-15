from PIL import Image, ImageDraw

class Maps:
    """
    users super maps creations
    """
    def __init__(self):
        self.__points = {'A1' : ((350, 575),(380, 605)),
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
        """
        create a copy of the basic map
        :param filename: the file name of a specific user
        :type: string
        """
        from shutil import copyfile
        src = r'D:\CYBER\Super List project\static\map.jpg'
        dst = r'D:\CYBER\Super List project\static\user_maps'
        dst +=  str(filename)
        copyfile(src, dst)

    def delete_last_copy(self, filename):
        """
        delete the last file with the name we get from the user_maps folder
        :param filename: the file name of a specific user
        :type: string
        """
        import glob
        import os
        try:
            id = filename.split("_")[0]
            path = r'static\user_maps'
            path += str(id) + "_*"
            arr = glob.glob(path)
            for url in arr:
                os.remove(url)
        except BaseException as e:
            print(e)


    def draw_points(self, mylist, filename):
        """
        create a super map for the user
        :param mylist: the user product's list
        :type: an array of dictionaries
        :param filename: the file name of a specific user
        :type: string
        """
        self.delete_last_copy(filename)
        self.make_a_copy(filename)
        path = r'D:\CYBER\Super List project\static\user_maps'
        path += filename
        im = Image.open(path)
        draw = ImageDraw.Draw(im)
        for product in mylist:
            place = str(product['shelf']) + str(product['pclass'])
            west_north = self.__points[place][0]
            east_south = self.__points[place][1]
            color = (6, 253, 39)
            draw.ellipse([west_north, east_south],fill=color, outline=color)
        im.save(path)

