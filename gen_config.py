import yaml

class generateConfig:
    def __init__(self, config_file):
        with open(config_file) as fl:
            self.data = yaml.load(fl)
        self.load_config()

    def load_config(self):
        data = self.data
        al = {}
        next_minos = []
        tetriminos = {}
        cnt = 0
        for d in data["tetriminos"].items():
            al.update({d[0]:d[1]["align"]})
            next_minos.append(d[0])
            tetriminos.update({d[0]:d[1]["form"]})

        self.SUPPRESS_NUM = data["suppress_num"]
        self.COND_NEXTMINO = data["condition_nextmino_judge"]
        self.ALIGN = al
        self.NEXT_MINOS = next_minos
        self.chip_size = data["puzzle_chip"]["size"]
        self.TETRIMINOS = tetriminos

    def gen_configfile(self):
        f = open("config_bombliss.py", "w")
        f.writelines("NEXT_MINOS = "+str(self.NEXT_MINOS)+"\n")
        f.writelines("WINDOW_POS = "+str(self.WINDOW_POS)+"\n")
        f.writelines("NEXT_POS = "+str(self.NEXT_POS)+"\n")
        f.writelines("NEXT_IMGS = "+str(self.NEXT_IMGS)+"\n")
        f.writelines("CHIP_X = "+str(self.chip_size[0])+"\n")
        f.writelines("CHIP_Y = "+str(self.chip_size[1])+"\n")
        f.writelines("ALIGN = "+str(self.ALIGN)+"\n")
        f.writelines("SUPPRESS_NUM = "+str(self.SUPPRESS_NUM)+"\n")
        f.writelines("COND_NEXTMINO = "+str(self.COND_NEXTMINO)+"\n")
        f.writelines("TETRIMINOS = "+str(self.TETRIMINOS)+"\n")
        f.close()

    @property
    def NEXT_MINOS(self):
        return self.NEXT_MINOS

    @property
    def CHIP_X(self):
        return self.chip_size[0]

    @property
    def CHIP_Y(self):
        return self.chip_size[1]

    @property
    def ALIGN(self):
        return self.ALIGN

    @property
    def WINDOW_POS(self):
        return self.data["window"]["board_position"] + self.data["window"]["board_size"]

    @property
    def NEXT_POS(self):
        return self.data["window"]["next_position"] + self.data["window"]["next_size"]

    @property
    def NEXT_IMGS(self):
        return [self.data["directory_next_imgs"]+x+"_binary.png" for x in self.NEXT_MINOS]

if __name__ == "__main__":
    c = generateConfig(config_file = "config_bombrite.yaml")
    c.load_config()
    c.gen_configfile()
    """
    print c.NEXT_MINOS
    print c.WINDOW_POS
    print c.NEXT_POS
    print c.NEXT_IMGS
    print c.CHIP_X, c.CHIP_Y
    print c.ALIGN
    #print c.TETRIMINOS
    """
