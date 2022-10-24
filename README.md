# French Locality Name Shortener - QGIS Plugin

Portage QGIS du programme [french-locality-name-shortener](https://github.com/bchartier/french-locality-name-shortener/tree/develop) de Benjamin et Julie CHARTIER permettant de créer des noms contractés de communes et arrondissements français.

Le plugin ajoute une fonction dans le moteur d'expression et un algorithme dans la boîte à outil.

![Screenshot showing shortened label](img/screenshot_label.png)

## TODO
- [x] Fonction dans le moteur d'expression
- [ ] Algorithme dans la toolbox


## Auto-name
``` sql
 CASE 
    WHEN (bounds_height( $geometry) / @map_scale) * 250 > length("NOM_COM")  
      THEN "NOM_COM"
    WHEN (bounds_height( $geometry) / @map_scale) * 250 > length(short_name("NOM_COM"))
      THEN short_name("NOM_COM")
    ELSE very_short_name("NOM_COM") 
END
-- Emprique, relation entre longueur de l'étiquette et largeur de la bbox/echelle à préciser
```

----

## License

Distributed under the terms of the [`MIT` license](LICENSE).
