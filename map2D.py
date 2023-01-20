# -*- coding: utf-8 -*-
"""
Brython GUI for leaflet map and various useful plugins

TODO :
    - parent_element doit être dans le document avant insertion de la carte leaflet sinon KO
    - régler le problème des load qui ne sont pas bons si on les mets dans un répertoire gui
"""

__author__ = "thierry.herve@free.fr"
__copyright__ = "Thierry Hervé"
__license__ = "MIT"

from browser import window, load, document, html
from bbox import BoundingBox

load("./leaflet/leaflet.js")
load("./leaflet/Leaflet.Editable.js")
load("./leaflet/leaflet.fullscreen.js")
load("./leaflet/Control.Geocoder.js")

load("./leaflet/jquery-3.6.0.min.js") # indispensable à scalefactor
load("./leaflet/leaflet.scalefactor.js")

load("./leaflet/leaflet-shades.js")
load("./leaflet/MapBoundingBox.js")


# plus explicite que 'L' utilisé dans leaflet !
leaflet = window.L # permet ensuite des appels direct au code javascript

# initialisation des stylesheets au chargement du module 
document <= html.LINK(rel="stylesheet", type="text/css", href="./leaflet/leaflet.css")
document <= html.LINK(rel="stylesheet", type="text/css", href="./leaflet/leaflet.fullscreen.css")
document <= html.LINK(rel="stylesheet", type="text/css", href="./leaflet/Control.Geocoder.css")

document <= html.LINK(rel="stylesheet", type="text/css", href="./leaflet/leaflet.scalefactor.css")

document <= html.LINK(rel="stylesheet", type="text/css", href="./leaflet/leaflet-shades.css")
    
class Map:
    
    def __init__(self,
            parent_element, id_html_elt, width, height, center, zoom, 
            minZoom=3, fullscreenControl=True, 
            maxBounds=[[-65.072130, -170.20238],[85.030870, 192.59761]] ,
            geocoder=True, scale=True, fullscreen=True, bounding_box=True,
            ):

        # tente de détruire l'élément carte si il existe afin 
        # de le récréer pour tenir compte des changements
        # éventuels d'options (sinon, leaflet remonte que la carte existe déjà)
        try:
            del document[id_html_elt]
        except KeyError:
            pass
            
        self.html_element = html.DIV(id=id_html_elt)
        self.html_element.style.width = width
        self.html_element.style.height = height
        parent_element <= self.html_element

        self.leaflet_map = leaflet.map(id_html_elt, {
            "editable": True,
            "center": center,
            "zoom": zoom, 
            "fullscreenControl": fullscreen,
            # limiter le zoom et l'emprise permet d'éviter le bug d'une mauvause
            # sélection d'emprise 
            "minZoom": minZoom,
            "maxBounds": maxBounds
        })


        leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?', {
            "attribution": 'Map data &copy; OpenStreetMap contributors'
        }).addTo(self.leaflet_map)

        if geocoder:
            leaflet.Control.geocoder().addTo(self.leaflet_map)
        if scale:
            leaflet.control.scalefactor().addTo(self.leaflet_map)
    
        
        if bounding_box:
            def handler(new_coords):
                for f in self._bind_functions:
                    f(new_coords)
            
            self._bounding_box = leaflet.control.map_bounding_box(handler)
            self._bounding_box.addTo(self.leaflet_map)
        else:
            self._bounding_box = None

        self._bind_functions = []
                    
    @property
    def bounding_box(self):
        if self._bounding_box is None: return None
        return BoundingBox(self._bounding_box.get())
        
    @bounding_box.setter
    def bounding_box(self, new_coords):
        # print('setter', new_coords)
        # print('old coords', getattr(self, 'X'))
        # old_coords = self._extent.get_extent()
        # print('old coords', old_coords)
         # if self.X == new_coords: return
        # if self._extent.get_extent() == new_coords: return
        self._bounding_box.set([v for v in new_coords])
    
    def bind(self, evt, function):
        self._bind_functions.append(function)
