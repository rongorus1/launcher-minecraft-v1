from components.progress_bar_generic import ProgressBarGeneric
from views.ram_configuration_window import RamConfigurationWindow


def open_window_configurar_ram(master = None, progressbar: ProgressBarGeneric = None):
    ram_window = RamConfigurationWindow(master = master if master else None, progress_bar = progressbar)