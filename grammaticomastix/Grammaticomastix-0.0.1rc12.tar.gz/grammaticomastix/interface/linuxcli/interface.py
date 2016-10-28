import logging
LOGGER = logging.getLogger(__name__)

def main_linuxcli(src_string):
    LOGGER.debug("main_linuxcli()")
    
    from gmastix import gmastix
    
    PROCESSES = gmastix.ProcessContainer()

    PROCESSES.add(gmastix.ProcessFRA0())
    PROCESSES.add(gmastix.ProcessFRA1())
    PROCESSES.add(gmastix.ProcessFRA2())
    PROCESSES.add(gmastix.ProcessFRA3())
    PROCESSES.add(gmastix.ProcessFRA4())
    PROCESSES.add(gmastix.ProcessFRA5ng())

    PROCESSES.add(gmastix.ProcessGRC0())
    PROCESSES.add(gmastix.ProcessGRC1())
    PROCESSES.add(gmastix.ProcessGRC2())
    PROCESSES.add(gmastix.ProcessGRC3())
    PROCESSES.add(gmastix.ProcessGRC4())
    PROCESSES.add(gmastix.ProcessGRC5ng())

    LECTOR = gmastix.Lector(src_string, PROCESSES)

    LOGGER.info(LECTOR)
    while LECTOR.read():
        LOGGER.info(LECTOR)

    LOGGER.debug("=== final state after %s turns ===", LECTOR.turn_number)
    LOGGER.debug(LECTOR)

    LOGGER.info("=== end ===")

    gmastix.colorprint(LECTOR.all_rhp.report())
    gmastix.colorprint("[default]=== end ===")

    gmastix.stop()
