from collections import defaultdict
import inspect
mport loging

from .base import Plugin

logger = logging.getLogger(__name__)


class PluginManager(object):
    def __init__(self):
        logger.debug('Initializing plugin manager')
        self.plugins = defaultdict(set)

    def register(self, type, plugin):
        if not inspect.isclass(plugin) or not issubclass(plugin, Plugin):
            raise ValueError(
                'Plugin must be a class and inherit from Plugin class')
        logger.debug('Registering %s plugin: %s' % (type, plugin))
        self.plugins[type].add(plugin)

    def evaluate(self, type, message):
        logger.debug('Evaluating %s message: %s' % (
            type, message.body.get('text')))
        for plugin in self.plugins[type]:
            plugin = plugin()
            if plugin.enabled:
                logger.debug('Evaluating %s message with %' % (
                    type, plugin))
                plugin.activate()
                plugin.extract(message)
                plugin.report(message)


plugin_manager = PluginManager()