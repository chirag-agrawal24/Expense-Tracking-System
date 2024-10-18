import logging

def setup_logger(name:str,log_file_path : str ="server.log",level=logging.DEBUG):
    #creating custom logger
    logger=logging.getLogger(name)

    logger.setLevel(level)
    file_handler=logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger