from views.ram_configuration_window import RamConfigurationWindow


def open_window_configurar_ram(master = None):
    ram_window = RamConfigurationWindow(master = master if master else None)