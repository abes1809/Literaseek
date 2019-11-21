$(function(){ 

		/** to hold layers for controller */

		var overlayMaps = {};

		/** base map */

		var map = L.map('organization_map').setView([41.881832, -87.623177], 13);

		var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
		   attribution: 'Map tiles by ' + '<a href="http://stamen.com">Stamen Design</a>' + ', under ' + '<a href="http://creativecommons.org/licenses/by/3.0">' + 'CC BY 3.0' + '</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>' + ', under' + '<a href="http://www.openstreetmap.org/copyright">ODbL</a>',
		   minZoom: 0,
		   maxZoom: 20,
		   ext: 'jpg'
		});

	    map.addLayer(Stamen_Terrain);

	    /** create map panes to set z index of layers */

	    map.createPane("pane250").style.zIndex = 250;
	    map.createPane("pane450").style.zIndex = 450;

	    /** create neighborhood layer */

		function get_neighborhood_data(){
	    	$.ajax({
	            url: 'http://localhost:5000/neighborhoods',
	            success: create_neighborhood_layer,
	            error: function(error){
	            	console.log(error)
	            }
	        });
	    }

	    function get_organization_marker_data(){

	    	var org_ids = $( "div.all_orgs" ).html();
	    	var org_ids = org_ids.split(',');

	    	for(let i = 0; i < org_ids.length; i++){
	    		org_ids[i] = org_ids[i].trim();
	    	}

	    	org_ids = {ids: org_ids};

	    	$.ajax({
	    		url: '/organization_data',
	    		type: "GET",
	    		data: org_ids,
	    		success: create_organization_layer,
	    		error: function(error){
	    			console.log(error)
	    		}
	    	});
	    }

	    function create_neighborhood_layer(result) {

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
		            pane: "pane250",
		            onEachFeature: onEachFeature
		        }).addTo(map)

		    overlayMaps["Neighborhoods"] = neighborhoods_layer;

		    create_map_layers();
	    };

	    function create_organization_layer(result) {

	    	var geojsonMarkerOptions = {
	    	            radius: 8,
	    	            fillColor: "grey",
	    	            color: "#000",
	    	            weight: 1,
	    	            opacity: 1,
	    	            fillOpacity: 1,
	    	        };

	        function onEachFeature(feature, layer) {
	            if (feature.properties && feature.properties.name && feature.properties.address){
	                layer.bindPopup("Organization Name: " + feature.properties.name + "Address: " + feature.properties.address);
	            }
	        };

	        var organizations_layer = L.geoJSON(result,
	        {
	            pointToLayer: function (feature, latlng) {
	                    return L.circleMarker(latlng, geojsonMarkerOptions);
	                },
	            pane: "pane450",
	            onEachFeature: onEachFeature
	        }
	        ).addTo(map)

	        overlayMaps["Organizations"] = organizations_layer;
	    };

	    /** stack all map layers */

	    function create_map_layers(){

	        baseMap = {
	            "terrain": Stamen_Terrain
	        };

	        L.control.layers(baseMap, overlayMaps).addTo(map);
	    };

	    get_organization_marker_data();
	    get_neighborhood_data();

})