from views.session_configuration_window import SessionConfigurationWindow


def run_session_controller(master = None):
    session_window = SessionConfigurationWindow(master = master if master else None)