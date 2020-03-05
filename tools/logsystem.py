import logging


class MyLog():
    plogger = logging.getLogger('Passenger')
    dlogger = logging.getLogger('Driver')
    mlogger = logging.getLogger()

    @staticmethod
    def init():
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)-17s [line:%(lineno)-3s] %(levelname)-7s %(name)-9s %(message)s',
                            datefmt='%Y %b %d %H:%M:%S',
                            filename='log.log',
                            filemode='w')

        #################################################################################################
        #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s   %(filename)-17s: %(levelname)-7s %(name)-9s %(message)s')
        console.setFormatter(formatter)
        MyLog.mlogger.addHandler(console)
        #################################################################################################
