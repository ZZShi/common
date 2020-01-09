# -*- coding: utf-8 -*-
"""
@Time       : 2020/1/9 1:24
@File       : logger.py
@Author     : ZZShi
@Difficulty ：
@Question   :
@Describe   :
"""
import os
import time
import logging
import logging.handlers


SMTP_INFO = {
    'mailhost': ('smtp.163.com', 25),
    'fromaddr': 'xxxxx@163.com',
    'toaddrs': ['xxxxx@qq.com'],
    'subject': 'Automation Robot',
    'credentials': ('xxxxx@163.com', '******')
}

COLORS = {
     'black': '30',
       'red': '31',
     'green': '32',
    'yellow': '33',
      'blue': '34',
    'purple': '35',
      'cyan': '36',
     'white': '37',
}


class Logger(object):
    """
    根据不同的日志等级在控制台输出不同的颜色
    """
    ch = logging.StreamHandler()

    def __init__(self, level=logging.DEBUG, file_handler=True, fh_level=None, smtp_handler=False, sh_level=logging.ERROR):
        """
        日志初始化
        :param level: 控制台日志等级
        :param file_handler: 启用日志文件
        :param fh_level: 日志文件等级
        :param smtp_handler: 启动日志邮箱
        :param sh_level: 日志邮箱等级
        """
        self.level = level
        self.fh_level = fh_level if fh_level else level
        self.sh_level = sh_level

        self.color_temp = '\033[0;{color}m{fmt}\033[0m'
        self.log_prefix = '[%(asctime)s][%(module)s][%(levelname)s] -> %(message)s'

        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        self.fmt = logging.Formatter(self.log_prefix)

        if file_handler:
            self.set_fh()
        if smtp_handler:
            self.set_sh()

    def set_fh(self):
        log_path = os.path.join(os.path.dirname(os.getcwd()), 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_file = os.path.join(log_path, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.log')

        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(self.fh_level)
        fh.setFormatter(self.fmt)
        self.logger.addHandler(fh)

    def set_sh(self):
        eh = logging.handlers.SMTPHandler(**SMTP_INFO)
        eh.setLevel(self.sh_level)
        eh.setFormatter(self.fmt)
        self.logger.addHandler(eh)

    def font_color(self, color):
        fmt_color = logging.Formatter(self.color_temp.format(color=color, fmt=self.log_prefix))
        self.ch.setFormatter(fmt_color)
        self.logger.addHandler(self.ch)

    def debug(self, msg):
        color = COLORS['green']
        self.font_color(color)
        self.logger.debug(msg)

    def info(self, msg):
        color = COLORS['purple']
        self.font_color(color)
        self.logger.info(msg)

    def warning(self, msg):
        color = COLORS['blue']
        self.font_color(color)
        self.logger.warning(msg)

    def critical(self, msg):
        color = COLORS['cyan']
        self.font_color(color)
        self.logger.critical(msg)

    def error(self, msg):
        color = COLORS['red']
        self.font_color(color)
        self.logger.error(msg)


if __name__ == '__main__':
    logger = Logger(file_handler=True, smtp_handler=True)
    words = 'China is stronger than American'.split()
    logger.debug(words[0])
    logger.info(words[1])
    logger.warning(words[2])
    logger.critical(words[3])
    logger.error(words[4])

