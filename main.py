import gen_config
g = gen_config.generateConfig(config_file="config/config_bombliss_snes_p2.yaml")
g.gen_configfile()
import BomblissMan

server = "192.168.10.148"
port = 50000

b = BomblissMan.BomblissMan(server, port)
b.go()
