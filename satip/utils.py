from slack_logger import SlackHandler, SlackFormatter
import logging

def set_up_logging(name: str, logging_level: str, 
                   log_fp: str, slack_webhook_url: str=None, 
                   slack_id: str=None) -> logging.Logger:
    """
    Initialises and configures the logger
    
    Parameters
    ----------
    name: str
        Name of the logger
    logging_level: str
        Logging level, must be one of: 
        'CRITICAL', 'FATAL', 'ERROR',
        'WARNING', 'WARN', 'INFO',
        'DEBUG' or 'NOTSET'
    log_fp: str
        Filepath where the logs will be stored

    Returns
    -------
    logger: logging.Logger
        Logger
    
    """
    
    # Initialising logger
    logger = logging.getLogger('helpers')
    
    # Configuring log level
    logging_levels = [
        'CRITICAL',
        'FATAL',
        'ERROR',
        'WARNING',
        'WARN',
        'INFO',
        'DEBUG',
        'NOTSET'
    ]
    
    assert logging_level in logging_levels, f"logging_level must be one of {', '.join(logging_levels)}"
    
    logger.setLevel(getattr(logging, logging_level))
    
    # Defining global formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Configuring Jupyter output handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Configuring file output handler
    file_handler = logging.FileHandler(log_fp, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Configuring slack output handler
    if (slack_webhook_url is not None) and (slack_id is not None):
        sh = SlackHandler(username='logger', icon_emoji=':robot_face:', url=slack_webhook_url, mention=slack_id)
        sf = SlackFormatter()
        sh.setFormatter(sf)
        sh.setLevel(logging.CRITICAL)
        logger.addHandler(sh)
    
    return logger