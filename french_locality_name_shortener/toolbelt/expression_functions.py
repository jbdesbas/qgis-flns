from qgis.utils import qgsfunction
from . import NameProcessor


class PlgFunction():
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
