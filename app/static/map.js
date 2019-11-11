$(function(){

	function get_neighborhood_data(){
    	$.ajax({
            url: 'http://localhost:5000/get_neighborhoods',
            success: create_neighborhood_layer,
            error: function(error){
            	console.log(error)
            }
        });
    }

	var map = L.map('program_map').setView([41.881832, -87.623177], 13);

    var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
	   attribution: 'Stamen',
	   minZoom: 0,
	   maxZoom: 20,
	   ext: 'jpg'
	});

    map.addLayer(Stamen_Terrain);

    function create_neighborhood_layer(result) {

	    // neighborhood layer style

	    function getColor(region_id) {
	    	console.log(region_id);
			if (region_id == 1) { 
				var color = 'red'
			} 
			else if (region_id == 2) { 
				var color = 'blue'
			}
			else if (region_id == 3) { 
				var color = 'green'
			}
			else if (region_id == 4) { 
				var color = 'yellow'
			}
			else if (region_id == 5) { 
				var color = 'grey'
			}
			else if (region_id == 6) { 
				var color = 'brown'
			}
			else if (region_id == 7) { 
				var color = 'purple'
			}
			else if (region_id == 8) { 
				var color = 'orange'
			}
			else if (region_id == 9) { 
				var color = 'teal'
			}

			return color
	    }

	    function zoomToFeature(e) {
	        map.fitBounds(e.target.getBounds());
	    }

	    function highlightFeature(e) {
	            var layer = e.target;

	            layer.setStyle({
	                weight: 5,
	                color: '#666',
	                dashArray: '',
	                fillOpacity: 0.7
	            });

	            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
	                layer.bringToFront();
	            }
	        };

	    function resetHighlight(e) {
	        console.log("fired");
	        neighborhoods_layer.resetStyle(e.target);
	    };

	    function style(feature) {
	        return {
	            fillColor: getColor(feature.properties.region_id),
	            weight: 2,
	            opacity: 1,
	            color: 'white',
	            dashArray: '3',
	            fillOpacity: 0.5,
	        };
	    };

	    function onEachFeature(feature, layer) {
	        if (feature.properties && feature.properties.name){
	            layer.bindPopup(feature.properties.name);
	        }
	        
	        layer.on({
	            mouseover: highlightFeature,
	            mouseout: resetHighlight,
	            click: zoomToFeature
	        });
	    };

	    var neighborhoods_layer = L.geoJSON(result,
	        {   
	            style: style,
	            onEachFeature: onEachFeature
	        }).addTo(map);
    };

    get_neighborhood_data();

});