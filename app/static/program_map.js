$(function(){

	/** additional page js **/
	var coll = document.getElementsByClassName("collapsible");
	var i;

	for (i = 0; i < coll.length; i++) {
	  coll[i].addEventListener("click", function() {
	    this.classList.toggle("active");
	    var content = this.nextElementSibling;
	    if (content.style.display === "block") {
	      content.style.display = "none";
	    } else {
	      content.style.display = "block";
	    }
	  });
	}

	/** base map */
	var map = L.map('program_map').setView([41.839232, -87.524748], 11);

    var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
	   attribution: 'Map tiles by ' + '<a href="http://stamen.com">Stamen Design</a>',
	   minZoom: 0,
	   maxZoom: 20,
	   ext: 'jpg'
	});

    map.addLayer(Stamen_Terrain);

    /** hover listener for program region highlight */

	function get_neighborhood_data(){
    	$.ajax({
            url: '/neighborhoods',
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
				var fillColor = '#D60F12'
			} 
			else if (region_id == 2) { 
				var fillColor = '#28A5E7'
			}
			else if (region_id == 3) { 
				var fillColor = '#43DE33'
			}
			else if (region_id == 4) { 
				var fillColor = '#D7F91E'
			}
			else if (region_id == 5) { 
				var fillColor = '#606060'
			}
			else if (region_id == 6) { 
				var fillColor = '#9C5209'
			}
			else if (region_id == 7) { 
				var fillColor = '#A10494'
			}
			else if (region_id == 8) { 
				var fillColor = '#FF8823'
			}
			else if (region_id == 9) { 
				var fillColor = '#6CEEEE'
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
	    	this.openPopup();

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
	    	this.closePopup();
	    	
	        neighborhoods_layer.resetStyle(e.target);
	    };

    	$('.program-card').hover(
			function(event) {

				var elem = $(event.currentTarget);
				console.log(elem);
				elem = elem[0]["childNodes"][1]["innerText"];
				get_program_region(elem);

				function get_program_region(elem){
			    	return $.ajax({
			            url: '/program_regions/' + elem,
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

    /** create legend */

    function getColor(region) {
    	console.log('fire');
		if (region == "Central") { 
			var color = 'red'
		} 
		else if (region == "Far North Side") { 
			var color = 'blue'
		}
		else if (region == "Far Southeast Side") { 
			var color = 'green'
		}
		else if (region == "Far Southwest Side") { 
			var color = 'yellow'
		}
		else if (region == "North Side") { 
			var color = 'grey'
		}
		else if (region == "Northwest Side") { 
			var color = 'brown'
		}
		else if (region == "South Side") { 
			var color = 'purple'
		}
		else if (region == "Southwest Side") { 
			var color = 'orange'
		}
		else if (region == "West Side") { 
			var color = 'teal'
		}

		return color
    }

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = ["Central", "Far North Side", "Far Southeast Side", "Far Southwest Side", "North Side", "Northwest Side", "South Side", "Southwest Side", "West Side"],
            labels = [];

        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '"></i> ' + grades[i] + '<br>';
        }

        return div;
    };

    legend.addTo(map);

});