import config.Properties
import logging

class Logger(logging.Logger):

    def __init__(self, class_name: str) -> None:
        super().__init__(class_name)
        level_by_config = config.Properties.Common().get_property("logger.level")
        print(f"Logger level ({level_by_config == 'INFO'}): {level_by_config}")
        logging.basicConfig(
            level=level_by_config, # DEBUG, INFO, WARNING, ERROR, CRITICAL
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

logging.setLoggerClass(Logger)