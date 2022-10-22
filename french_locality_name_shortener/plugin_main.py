#! python3  # noqa: E265

"""
    Main plugin module.
"""

# PyQGIS
from qgis.core import QgsApplication, QgsExpression
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import showPluginHelp

# project
from french_locality_name_shortener.__about__ import __title__

from french_locality_name_shortener.processing import FrenchLocalityNameShortenerProvider

from french_locality_name_shortener.toolbelt import PlgLogger, PlgTranslator, PlgFunction

# ############################################################################
# ########## Classes ###############
# ##################################


class FrenchLocalityNameShortenerPlugin:
    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.log = PlgLogger().log
        self.provider = None

        # translation
        plg_translation_mngr = PlgTranslator()
        translator = plg_translation_mngr.get_translator()
        if translator:
            QCoreApplication.installTranslator(translator)
        self.tr = plg_translation_mngr.tr

    def initGui(self):

        # -- Function
        QgsExpression.registerFunction(PlgFunction.short_name) # A factoriser dans expression_functions.py
        QgsExpression.registerFunction(PlgFunction.very_short_name)

        # -- Processing
        self.initProcessing()

    
    def initProcessing(self):
        self.provider = FrenchLocalityNameShortenerProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        # -- Unregister processing
        QgsApplication.processingRegistry().removeProvider(self.provider)

        # -- Unregister functions
        QgsExpression.unregisterFunction('short_name') # A factoriser dans expression_functions.py
        QgsExpression.unregisterFunction('very_short_name')

    def run(self):
        """Main process.

        :raises Exception: if there is no item in the feed
        """
        try:
            self.log(
                message=self.tr(
                    text="Everything ran OK.",
                    context="FrenchLocalityNameShortenerPlugin",
                ),
                log_level=3,
                push=False,
            )
        except Exception as err:
            self.log(
                message=self.tr(
                    text="Houston, we've got a problem: {}".format(err),
                    context="FrenchLocalityNameShortenerPlugin",
                ),
                log_level=2,
                push=True,
            )
