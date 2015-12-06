def print_time(undecorated_function):
    """Print time spent by decorated function
    :param undecorated_function: function to be decorated
    """
    import functools
    import time
    from log import create_logger

    logger = create_logger(name=undecorated_function.__name__)

    @functools.wraps(undecorated_function)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = undecorated_function(*args, **kwargs)
        spent_time = time.time() - start_time
        logger.info('executed in {0:g} sec'.format(spent_time))
        return result

    return decorated_function
