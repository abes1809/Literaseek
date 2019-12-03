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

		/** to hold layers for controller */

		var overlayMaps = {};

		/** base map */

		var map = L.map('organization_map').setView([41.881832, -87.623177], 13);

		var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
		   attribution: 'Map tiles by ' + '<a href="http://stamen.com">Stamen Design</a>',
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
	            url: '/neighborhoods',
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

	    	function open_on_hover(organization){	  
	    		organizations_layer.eachLayer(function (layer) {
	    			var popup_name = layer['feature']['properties']['name'];
	    			var lat = layer['_latlng']['lat'];
	    			var lng = layer['_latlng']['lng'];

    				if (organization == popup_name){
    					map.panTo([lat, lng], 15);
    					layer.openPopup()
	    			}
	    		});
	    	}

    	    function close_popup_hover(){
    	    	organizations_layer.eachLayer(function (layer) {
    				layer.closePopup();	
    	    	});
    	    }

	    	$('.program-card').hover(
				function(event) {
					var elem = $(event.currentTarget);
					console.log(elem);
					elem = elem[0]["childNodes"][3]["innerText"];
					console.log(elem);
					open_on_hover(elem);	
				},
				function(event){
					close_popup_hover();
				}
	    	);

	    	function openPopUp(e) {
	    		this.openPopup();
	    	}

	    	function closePopUp(e) {
	    		this.closePopup();
	    	}

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

	            layer.on({
                	mouseover: openPopUp,
    	        	mouseout: closePopUp,
	            });
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

})