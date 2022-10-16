# French Locality Name Shortener - QGIS Plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


[![flake8](https://img.shields.io/badge/linter-flake8-green)](https://flake8.pycqa.org/)

Portage QGIS du programme [french-locality-name-shortener](https://github.com/bchartier/french-locality-name-shortener/tree/develop) de Benjamin et Julie CHARTIER permettant de créer des noms contractés de communes et arrondissements français.

Le plugin ajoute une fonction dans le moteur d'expression et un algorithme dans la boîte à outil.

## Generated options

### Plugin

"plugin_name": French Locality Name Shortener
"plugin_name_slug": french_locality_name_shortener
"plugin_name_class": FrenchLocalityNameShortener

"plugin_category": Vector
"plugin_description_short": Ce programme crée les noms contractés des communes françaises.
"plugin_description_long": Ce programme crée les noms contractés des communes françaises.
"plugin_description_short": Ce programme crée les noms contractés des communes françaises.
"plugin_icon": default_icon.png

"author_name": Benjamin CHARTIER, Julie CHARTIER, Jean-Baptiste DESBAS
"author_email": qgis@company.com

"qgis_version_min": 3.22
"qgis_version_max": 3.99

### Tooling

This project is configured with the following tools:

- [Black](https://black.readthedocs.io/en/stable/) to format the code without any existential question
- [iSort](https://pycqa.github.io/isort/) to sort the Python imports

Code rules are enforced with [pre-commit](https://pre-commit.com/) hooks.  
Static code analisis is based on: Flake8

See also: [contribution guidelines](CONTRIBUTING.md).

## CI/CD

Plugin is linted, tested, packaged and published with GitHub.

If you mean to deploy it to the [official QGIS plugins repository](https://plugins.qgis.org/), remember to set your OSGeo credentials (`OSGEO_USER_NAME` and `OSGEO_USER_PASSWORD`) as environment variables in your CI/CD tool. 


### Documentation

The documentation is generated using Sphinx and is automatically generated through the CI and published on Pages.

- homepage: <https://github.com/bchartier/french-locality-name-shortener/>
- repository: <https://github.com/bchartier/french-locality-name-shortener/>
- tracker: <https://github.com/bchartier/french-locality-name-shortener//issues>

----

## License

Distributed under the terms of the [`MIT` license](LICENSE).
