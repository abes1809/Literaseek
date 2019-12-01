$(function(){

	/** base map */
	var map = L.map('program_map').setView([41.881832, -87.623177], 11);

    var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
	   attribution: 'Stamen',
	   minZoom: 0,
	   maxZoom: 20,
	   ext: 'jpg'
	});

    map.addLayer(Stamen_Terrain);

    /** hover listener for program region highlight */

	function get_neighborhood_data(){
    	$.ajax({
            url: 'http://localhost:5000/neighborhoods',
            success: create_neighborhood_layer,
            error: function(error){
            	console.log(error)
            }
        });
    }

    function create_neighborhood_layer(result) {

	    // neighborhood layer style

	    function create_highlights(program_regions){	  
	    	neighborhoods_layer.eachLayer(function (layer) {
	    		var layer_region_id = layer['feature']['properties']['region_id'];
	    		for (let i in program_regions) {
	    			if (program_regions[i]['id'] == layer_region_id){
	    				layer.setStyle({fillColor: get_highlight_color(layer_region_id)})
	    			}
	    		}
	    	});
	    }

	    function reset_highlight(){
	    	neighborhoods_layer.eachLayer(function (layer) {
	    		var layer_region_id = layer['feature']['properties']['region_id'];
				layer.setStyle({fillColor: getColor(layer_region_id)})	
	    	});
	    }

	    function get_highlight_color(region_id){
	    	if (region_id == 1) { 
				var fillColor = '#fc9272'
			} 
			else if (region_id == 2) { 
				var fillColor = '#9ecae1'
			}
			else if (region_id == 3) { 
				var fillColor = '#a1d99b'
			}
			else if (region_id == 4) { 
				var fillColor = '#edf8b1'
			}
			else if (region_id == 5) { 
				var fillColor = '#bdbdbd'
			}
			else if (region_id == 6) { 
				var fillColor = '#987654'
			}
			else if (region_id == 7) { 
				var fillColor = '#9ebcda'
			}
			else if (region_id == 8) { 
				var fillColor = '#fdae6b'
			}
			else if (region_id == 9) { 
				var fillColor = '#a6bddb'
			}

			return fillColor
	    }

	    function getColor(region_id) {
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

    	$('.program').hover(
			function(event) {

				var elem = $(event.currentTarget);
				elem = elem[0]["childNodes"][3]["innerText"];
				get_program_region(elem);

				function get_program_region(elem){
			    	return $.ajax({
			            url: 'http://localhost:5000/program_regions/' + elem,
			            success: function(data){
			            	var program_regions = data[0]['regions'];
			            	create_highlights(program_regions);
			            },
			            error: function(error){
			            	console.log(error)
			            }
			        });
			    };

			},
			function(event){
				reset_highlight();
			}
    	);

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