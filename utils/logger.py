import logging
import sys

# Define custom log level for UI updates that we don't want mixing with standard logs
UI_LEVEL_NUM = 25
logging.addLevelName(UI_LEVEL_NUM, "UI")

def ui(self, message, *args, **kws):
    if self.isEnabledFor(UI_LEVEL_NUM):
        self._log(UI_LEVEL_NUM, message, args, **kws)
logging.Logger.ui = ui

class TerminalFormatter(logging.Formatter):
    COLORS = {
        'WARNING': '\033[93m',
        'INFO': '\033[94m',
        'DEBUG': '\033[90m',
        'CRITICAL': '\033[91m',
        'ERROR': '\033[91m'
    }
    RESET = '\033[0m'

    def format(self, record):
        if record.levelname == "UI":
            return record.getMessage()
        log_fmt = f"[{self.COLORS.get(record.levelname, '')}{record.levelname}{self.RESET}] {record.getMessage()}"
        return log_fmt

def setup_logger():
    logger = logging.getLogger("spectre")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate logs if setup is called multiple times
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(TerminalFormatter())
        logger.addHandler(ch)
    
    return logger

log = setup_logger()
