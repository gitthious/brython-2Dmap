/*
Add to leaflet.map a bounding box selector.
use leaflet-shades leaflet plugin (https://github.com/mkong0216/leaflet-shades)

Usage :

    var map = L.map('carte', {
                "editable": True, // indispensable !
            });
            
    function handler(selected_area) {
           // called when bounding_box is changed
           // selected_area is array[] de 4 float of bounding_box
           // latSW, longSW, latNE, longNE
    }

    leaflet.control.map_bounding_box(handler).addTo(map);

    expose get() and set() method to respectivly get and set selected area.
*/

if (typeof window.L === 'undefined') {
    throw new Error('Leaflet must be loaded first');
}

L.control.map_bounding_box = function (change_handler) {
    return new MapBoundingBox(change_handler);
};
 
MapBoundingBox = function(change_handler) {

    var the_shade = null;
    var the_rect = null;
    var the_map = null;
    
    L.EditControl = L.Control.extend({

        options: {
            position: 'topleft',
            callback: null,
            kind: '',
            html: ''
        },

        onAdd: function (map) {
            var container = L.DomUtil.create('div', 'leaflet-control leaflet-bar'),
                link = L.DomUtil.create('a', '', container);

            link.href = '#';
            link.title = "Définir une emprise ou l'effacer";
            link.innerHTML = this.options.html;
            L.DomEvent.on(link, 'click', L.DomEvent.stop)
                      .on(link, 'click', function () {
							if( the_shade ) {
								map.removeLayer(the_shade);
								the_shade = null;
								if( the_rect){
									map.removeLayer(the_rect);
									the_rect = null;
								}
							}
							the_shade = new L.leafletShades();
                            
							the_shade.on("shades:bounds-changed", function(e) {
									change_handler([
                                        e.bounds.getSouthWest().lat,  e.bounds.getSouthWest().lng,
                                        e.bounds.getNorthEast().lat, e.bounds.getNorthEast().lng
                                    ])
								});
							the_shade.addTo(map); 
							window.LAYER = this.options.callback.call(map.editTools);
                      }, this);

            return container;
        }



    });
    

    this.addTo = function (map) {
        the_map = map
        map.on("editable:drawing:commit", function(e) {
            the_rect = e.layer;
        });

        L.NewRectangleControl = L.EditControl.extend({

            options: {
                position: 'topleft',
                callback: map.editTools.startRectangle,
                html: "<span style='font-size:30px;'>&#9744;</span>"//'☐'
            }

        });
        
        map.addControl(new L.NewRectangleControl());
    }
    
    this.set = function (coords) {
        
        var p1 = L.latLng(coords[0], coords[1]);
        var p2 = L.latLng(coords[2], coords[3]);
        var bounds = L.latLngBounds([p1, p2]);

        if( the_shade ) {
            the_map.removeLayer(the_shade);
            
            if( the_rect){
                the_map.removeLayer(the_rect);
            }
        }
        the_rect = L.rectangle([p1, p2]).addTo(the_map);
        the_rect.enableEdit();
        the_shade = new L.LeafletShades({ bounds: the_rect.getBounds() });
        bounds = the_rect.getBounds()
        change_handler([
            bounds.getSouthWest().lat,  bounds.getSouthWest().lng,
            bounds.getNorthEast().lat, bounds.getNorthEast().lng
        ])
        
        the_shade.on("shades:bounds-changed", function(e) {
            change_handler([
                e.bounds.getSouthWest().lat,  e.bounds.getSouthWest().lng,
                e.bounds.getNorthEast().lat, e.bounds.getNorthEast().lng
            ])
        });
        the_shade.addTo(the_map); 
    }

    this.get = function () {
        if(! the_rect) {  return null; }
        
        bounds = the_rect.getBounds()
        return [
            bounds.getSouthWest().lat,  bounds.getSouthWest().lng,
            bounds.getNorthEast().lat, bounds.getNorthEast().lng
        ]
    }
}
