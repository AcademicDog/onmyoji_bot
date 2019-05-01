import logging

class WriteLog:
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s  %(filename)s  [line:%(lineno)d]  %(levelname)s  %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename='log.log',
            filemode='w')

    #################################################################################################
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
    
    def writeinfo(self, *args, **kwargs):
        logging.info(*args, **kwargs)
    
    def writewarning(self, *args, **kwargs):
        logging.warning(*args, **kwargs)

    def writedebug(self, *args, **kwargs):
        logging.debug(*args, **kwargs)