from slack_logger import SlackHandler, SlackFormatter
import logging

def create_markdown_table(table_info: dict, index_name: str='Id') -> str:
    """
    Returns a string for a markdown table, formatted
    according to the dictionary passed as `table_info` 
    
    Parameters:
        table_info: Mapping from index to values
        index_name: Name to use for the index column

    Returns:
        md_str: Markdown formatted table string  

    Example:
        >>> table_info = {
                'Apples': {
                    'Cost': '40p',
                    'Colour': 'Red/green',
                },
                'Oranges': {
                    'Cost': '50p',
                    'Colour': 'Orange',
                },
            }
        >>> md_str = create_markdown_table(table_info, index_name='Fruit')
        >>> print(md_str) 
        | Fruit   | Cost   | Colour    |
        |:--------|:-------|:----------|
        | Apples  | 40p    | Red/green |
        | Oranges | 50p    | Orange    |
    
    """
    
    df_info = pd.DataFrame(table_info).T
    df_info.index.name = index_name
    
    md_str = df_info.to_markdown()
    
    return md_str

def set_up_logging(name: str, log_fp: str, 
                   main_logging_level: str='DEBUG', 
                   slack_logging_level: str='CRITICAL', 
                   slack_webhook_url: str=None, slack_id: str=None) -> logging.Logger:
    """
    `set_up_logging` initialises and configures a custom
    logger for `satip`. The logging level of the file and 
    Jupyter outputs are specified by `main_logging_level`
    whilst the Slack handler uses `slack_logging_level`.
    
    There are three core ways that logs are broadcasted:
    
    - Logging to a specified file
    - Logging to Jupyter cell outputs
    - Logging to Slack
    
    Note that the value passed for `main_logging_level` 
    and `slack_logging_level` must be one of: 
    
    - 'CRITICAL'
    - 'FATAL'
    - 'ERROR'
    - 'WARNING'
    - 'WARN'
    - 'INFO'
    - 'DEBUG'
    - 'NOTSET'
    
    Parameters:
        name: Name of the logger
        log_fp: Filepath where the logs will be stored
        main_logging_level: Logging level for file and Jupyter
        slack_logging_level: Logging level for Slack
        slack_webhook_url: Webhook for the log Slack channel
        slack_id: Option user-id to mention in Slack

    Returns:
        logger: Custom satip logger

    Example:
        Here we'll create a custom logger that saves data
        to the file 'test_log.txt' and also sends Slack
        messages to the specified user and channel.

        >>> from satip.utils import set_up_logging
        >>> import logging
        >>> logger = set_up_logging('test_log', 
                                    'test_log.txt', 
                                    slack_id=slack_id,
                                    slack_webhook_url=slack_webhook_url)
        >>> logger.log(logging.INFO, 'This will output to file and Jupyter but not to Slack as it is not critical')
        '2020-10-20 10:24:35,367 - INFO - This will output to file and Jupyter but not to Slack as it is not critical'
    
    """
    
    # Initialising logger
    logger = logging.getLogger(name)
    
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
    
    assert main_logging_level in logging_levels, f"main_logging_level must be one of {', '.join(logging_levels)}"
    assert slack_logging_level in logging_levels, f"slack_logging_level must be one of {', '.join(logging_levels)}"
    
    logger.setLevel(getattr(logging, main_logging_level))
    
    # Defining global formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Configuring Jupyter output handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Configuring file output handler
    file_handler = logging.FileHandler(log_fp, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, main_logging_level))
    logger.addHandler(file_handler)

    # Configuring slack output handler
    if slack_webhook_url is not None:
        slack_handler = SlackHandler(username='logger', url=slack_webhook_url, mention=slack_id)
        slack_handler.setFormatter(SlackFormatter())
        slack_handler.setLevel(getattr(logging, slack_logging_level))
        logger.addHandler(slack_handler)
    
    return logger