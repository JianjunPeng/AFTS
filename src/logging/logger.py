import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..config.config import Config

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        config = Config.get()
        self.logger = logging.getLogger("afts")
        self.logger.setLevel(config.log_level)

        # Avoid adding multiple handlers if Logger is instantiated multiple times
        if self.logger.handlers:
            return
        
        level_map = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING,
                     "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}

        # Console handler (always show)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)  # Console can show all levels
        console.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        )
        self.logger.addHandler(console)

        # File handler with rotation
        if config.log_file:
            log_path = Path(config.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                config.log_file,
                maxBytes=config.log_max_size,
                backupCount=config.log_backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level_map.get(config.log_level, logging.INFO))
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
                )
            )
            self.logger.addHandler(file_handler)

    # Methods to log at different levels
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level: str, message: str):
        """
        level: INFO / WARNING / ERROR / CRITICAL
        message: Event description
        """
        level = level.upper()
        if level not in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
            level = "INFO"
        match level:
            case "DEBUG":
                self.debug(message)
            case "INFO":
                self.info(message)
            case "WARNING":
                self.warning(message)
            case "ERROR":
                self.error(message)
            case "CRITICAL":
                self.critical(message)

    @classmethod
    def get(cls):
        return cls()
    

# For testing purposes
if __name__ == "__main__":
    logger = Logger()
    logger.info("test...")
    logger.debug("test...")
    logger.warning("test...")
    logger.error("test...")
    logger.critical("test...")

