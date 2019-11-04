$(function(){

	var map = L.map('program_map').setView([41.881832, -87.623177], 13);

    var Stamen_Terrain = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
	   attribution: 'Stamen',
	   minZoom: 0,
	   maxZoom: 20,
	   ext: 'jpg'
	});

    map.addLayer(Stamen_Terrain);

});