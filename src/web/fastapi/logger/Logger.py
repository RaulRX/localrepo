from ..config.Properties import Common
import logging

class Logger(logging.Logger):

    # Fix pragmatico. En vez de configurarlo manualmente, usar el logging de python
    __configured = False

    def __init__(self, class_name: str) -> None:
        super().__init__(class_name)
        if not Logger.__configured:
            level_by_config = Common().get_property("logger.level")
            print(f"Logger level: {level_by_config}")
            logging.basicConfig(
                level=level_by_config, # DEBUG, INFO, WARNING, ERROR, CRITICAL
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        Logger.__configured = True

logging.setLoggerClass(Logger)