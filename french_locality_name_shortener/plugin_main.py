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
from qgis.utils import showPluginHelp, qgsfunction

# project
from french_locality_name_shortener.__about__ import __title__
from french_locality_name_shortener.gui.dlg_settings import PlgOptionsFactory

from french_locality_name_shortener.processing import FrenchLocalityNameShortenerProvider

from french_locality_name_shortener.toolbelt import PlgLogger, PlgTranslator, NameProcessor

# ############################################################################
# ########## Classes ###############
# ##################################


@qgsfunction(args='auto', group='French Locality Name Shortener')
def short_name(string, feature, parent):
    """
    Nom court de la commune
    <h4>Syntax</h4>
    <p><strong>short_name</strong>(<i>name</i>)
    <h4>Example usage</h4>
    <p>short_name('Saint-Paul-de-Vence') -> 'St-Paul-de-V.'
    """
    return NameProcessor(string).get_short_name()


@qgsfunction(args='auto', group='French Locality Name Shortener')
def very_short_name(string, feature, parent):
    """
    Nom très court de la commune
    <h4>Syntax</h4>
    <p><strong>very_short_name</strong>(<i>name</i>)
    <h4>Example usage</h4>
    <p>very_short_name('Saint-Paul-de-Vence') -> 'St-Paul'
    """
    return NameProcessor(string).get_very_short_name()



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
        """Set up plugin UI elements."""

        # settings page within the QGIS preferences menu
        self.options_factory = PlgOptionsFactory()
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        # -- Actions
        self.action_help = QAction(
            QIcon(":/images/themes/default/mActionHelpContents.svg"),
            self.tr("Help", context="FrenchLocalityNameShortenerPlugin"),
            self.iface.mainWindow(),
        )
        self.action_help.triggered.connect(
            lambda: showPluginHelp(filename="resources/help/index")
        )

        self.action_settings = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Settings"),
            self.iface.mainWindow(),
        )
        self.action_settings.triggered.connect(
            lambda: self.iface.showOptionsDialog(
                currentPage="mOptionsPage{}".format(__title__)
            )
        )

        # -- Menu
        self.iface.addPluginToMenu(__title__, self.action_settings)
        self.iface.addPluginToMenu(__title__, self.action_help)

        # -- Function
        QgsExpression.registerFunction(short_name)
        QgsExpression.registerFunction(very_short_name)

        # -- Processing
        self.initProcessing()

    
    def initProcessing(self):
        self.provider = FrenchLocalityNameShortenerProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        """Cleans up when plugin is disabled/uninstalled."""
        # -- Clean up menu
        self.iface.removePluginMenu(__title__, self.action_help)
        self.iface.removePluginMenu(__title__, self.action_settings)

        # -- Clean up preferences panel in QGIS settings
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

        # -- Unregister processing
        QgsApplication.processingRegistry().removeProvider(self.provider)

        # -- Unregister functions
        QgsExpression.unregisterFunction('short_name')
        QgsExpression.unregisterFunction('very_short_name')

        # remove actions
        del self.action_settings
        del self.action_help

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
