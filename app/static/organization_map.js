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

		var map = L.map('organization_map').setView([41.839232, -87.524748], 11);

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

	    	$('.legend-color').hover(
				function(event) {
					var elem = $(event.currentTarget);
					console.log(elem);
					elem = elem[0]["style"]["background"];
					console.log(elem);
					create_highlight_legend(elem);

				},
				function(event){
					reset_highlight_hover();
				}
	    	);

		    function create_highlight_legend(background_color) {
		    	    	console.log(background_color);
		    	    	program_region = get_region_id(background_color);
		    	    	neighborhoods_layer.eachLayer(function (layer) {
		    	    		var layer_region_id = layer['feature']['properties']['region_id'];
		        			if (program_region == layer_region_id){
		        				layer.setStyle({fillColor: get_highlight_color(layer_region_id)})
		        			}
		    	    	});
		    	    }

    	    function reset_highlight_hover(){
    	    	neighborhoods_layer.eachLayer(function (layer) {
    	    		var layer_region_id = layer['feature']['properties']['region_id'];
    				layer.setStyle({fillColor: getColor(layer_region_id)})	
    	    	});
    	    }

    	    function get_region_id(background_color){
    			if (background_color == 'rgb(252, 146, 114)') { 
    				/** red **/
    				var region = 1
    			} 
    			else if (background_color == 'rgb(158, 202, 225)') { 
    				/** blue **/
    				var region = 2
    			}
    			else if (background_color == 'rgb(161, 217, 155)') { 
    				/** green **/
    				var region = 3
    			}
    			else if (background_color == 'rgb(255, 237, 160)') { 
    				/** yellow **/
    				var region = 4
    			}
    			else if (background_color == 'rgb(150, 150, 150)') { 
    				/** grey **/
    				var region = 5
    			}
    			else if (background_color == 'rgb(254, 196, 79)') { 
    				/** brown **/
    				var region = 6
    			}
    			else if (background_color == 'rgb(136, 86, 167)') { 
    				/** purple **/
    				var region = 7
    			}
    			else if (background_color == 'rgb(201, 148, 199)') { 
    				/** pink **/
    				var region = 8
    			}
    			else if (background_color == 'rgb(65, 182, 196)') { 
    				/** teal **/
    				var region = 9
    			}

    			return region
    	    }

    	    function get_highlight_color(region_id){
    	    	if (region_id == 1) { 
    				var fillColor = '#de2d26'
    			} 
    			else if (region_id == 2) { 
    				var fillColor = '#3182bd'
    			}
    			else if (region_id == 3) { 
    				var fillColor = '#31a354'
    			}
    			else if (region_id == 4) { 
    				var fillColor = '#feb24c'
    			}
    			else if (region_id == 5) { 
    				var fillColor = '##bdbdbd'
    			}
    			else if (region_id == 6) { 
    				var fillColor = '#d95f0e'
    			}
    			else if (region_id == 7) { 
    				var fillColor = 'rgb(92, 1, 148)'
    			}
    			else if (region_id == 8) { 
    				var fillColor = '#dd1c77'
    			}
    			else if (region_id == 9) { 
    				var fillColor = '#056c59'
    			}

    			return fillColor
    	    }

    	    function getColor(region_id) {
    			if (region_id == 1) { 
    				/** red **/
    				var color = 'rgb(252, 146, 114)'
    			} 
    			else if (region_id == 2) { 
    				/** blue **/
    				var color = 'rgb(158, 202, 225)'
    			}
    			else if (region_id == 3) { 
    				/** green **/
    				var color = 'rgb(161, 217, 155)'
    			}
    			else if (region_id == 4) { 
    				/** yellow **/
    				var color = 'rgb(255, 237, 160)'
    			}
    			else if (region_id == 5) { 
    				/** grey **/
    				var color = 'rgb(150, 150, 150)'
    			}
    			else if (region_id == 6) { 
    				/** brown **/
    				var color = 'rgb(254, 196, 79)'
    			}
    			else if (region_id == 7) { 
    				/** purple **/
    				var color = 'rgb(136, 86, 167)'
    			}
    			else if (region_id == 8) { 
    				/** pink **/
    				var color = 'rgb(201, 148, 199)'
    			}
    			else if (region_id == 9) { 
    				/** teal **/
    				var color = 'rgb(65, 182, 196)'
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
    					map.flyTo([lat, lng],13, {animate: true});
    					layer.openPopup();
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
	    	            fillColor: "#174039",
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

   		if (region == "Far North Side") { 
   			/** blue **/
   			var color = '#9ecae1'
   		} 
   		else if (region == "North Side") {
   			/** grey **/ 
   			var color = '#969696'
   		}
   		else if (region == "Northwest Side") { 
   			/** brown **/
   			var color = '#fec44f'
   		}
   		else if (region == "Central") {
   			/** red **/
   			var color = '#fc9272'
   		}
   		else if (region == "West Side") { 
   			/** teal **/
   			var color = '#41b6c4'
   		}
   		else if (region == "South Side") { 
   			/** purple **/
   			var color = 'rgb(136, 86, 167)'
   		}
   		else if (region == "Southwest Side") {
   			/** pink **/ 
   			var color = '#c994c7'
   		}
   		else if (region == "Far Southeast Side") {
   			/** green **/ 
   			var color = '#a1d99b'
   		}
   		else if (region == "Far Southwest Side") {
   			/** yellow **/ 
   			var color = '#ffeda0'
   		}

   		return color
       }

       var legend = L.control({position: 'bottomright'});

       legend.onAdd = function (map) {

           var div = L.DomUtil.create('div', 'info legend'),
               grades = ["Far North Side", "North Side", "Northwest Side", "Central", "West Side", "South Side", "Southwest Side", "Far Southeast Side", "Far Southwest Side"],
               labels = ['<strong>Chicago Regions</strong>'];

           for (var i = 0; i < grades.length; i++) {
           	div.innerHTML += 
           	labels.push(
           	'<i class="legend-color" style="background:' + getColor(grades[i]) + '"></i> ' + (grades[i] ? grades[i] : '+')
           	);
           	div.innerHTML = labels.join('<br>');
           }

           return div;
       };

       legend.addTo(map);

})