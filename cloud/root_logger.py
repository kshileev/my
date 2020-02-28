def create_base_logger(name):
    import logging
    import os

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler_candidates = [x for x in logger.handlers if type(x) == logging.StreamHandler]
    file_handler_candidates = [x for x in logger.handlers if type(x) == logging.FileHandler]
    formatter = logging.Formatter(fmt='{name}: {message}', style='{')
    if len(stream_handler_candidates) == 0:
        st_hdl = logging.StreamHandler()
        st_hdl.setLevel(logging.DEBUG)
        st_hdl.setFormatter(fmt=formatter)
        logger.addHandler(st_hdl)
    if len(file_handler_candidates) == 0:
        os.system('mkdir -p artifacts')
        file_hdl = (logging.FileHandler(filename=os.path.join('artifacts', name + '_debug.log'), mode='w'))
        file_hdl.setLevel(logging.DEBUG)
        file_hdl.setFormatter(fmt=formatter)
        logger.addHandler(file_hdl)
    logger.info('main pod logger created')


def create_component_logger(name):
    import logging

    root_logger_name  = name.split('.')[0]

    root_logger = logging.getLogger(root_logger_name)
    if not root_logger.handlers:
        create_base_logger(root_logger_name)
    logger = logging.getLogger(name)
    logger.info('logger created')
    return logger