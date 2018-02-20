import sys
import os

try:
    from archan import Provider, Argument, DMM, Logger
    from pylint.lint import Run


    class LoggerWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message):
            if message != '\n':
                self.level(message)


    class MessagesPerModule(Provider):
        """Pylint provider for Archan."""

        identifier = 'archan_pylint.MessagesPerModule'
        name = 'Messages per Module'
        description = 'Number of Pylint messages per module.'
        arguments = (
            Argument('pylint_args', list, 'Pylint arguments as a list.'),
            Argument('depth', int, 'The depth of the matrix to generate.'),
        )

        def get_dsm(self, pylint_args=None, depth=None):
            """
            Provide matrix data for Pylint messages in a set of packages.

            Args:
                pylint_args (list): the arguments to pass to Pylint.
                depth (int): the depth of the matrix to generate.

            Returns:
                archan.DSM: instance of archan DSM.
            """
            logger = Logger.get_logger(__name__)
            pylint_args = pylint_args or []

            sys.stdout = LoggerWriter(logger.debug)
            sys.stderr = LoggerWriter(logger.warning)

            try:
                run = Run(pylint_args, do_exit=False)
            except TypeError:
                run = Run(pylint_args, exit=False)

            sys.stdout = sys.__stdout__
            sys.sterr = sys.__stderr__

            entities = []
            data = []
            for k, v in run.linter.stats['by_module'].items():
                entities.append(k)
                data.append([sum(v.values())])
            entities.append('Messages')

            return DMM(data=data, entities=entities)

except ImportError:
    class MessagesPerModule():
        """Empty provider, please install Archan and Pylint."""
