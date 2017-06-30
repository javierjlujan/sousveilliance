// map variable
var map

// URL of the tile
var urlTile = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
// CopyLeft of the map
var mapAtribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';

map = L.map('mapid').setView([-34.60, -58.40], 13);

L.tileLayer(urlTile, {
    attribution: mapAtribution,
    maxZoom: 18
}).addTo(map);

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "cantidad_por_coord.csv",
        dataType: "text",
        success: function(data) {processData(data);}
     });
});

var data;
function processData(csv) {
    data = $.csv.toObjects(csv);

    for (point of data) {
	var circle = L.circle([point.lat, point.lon], {
	    color: 'red',
	    fillColor: '#f03',
	    fillOpacity: 0.5,
	    radius: 0.3 * parseInt(point.cantidad)
	})
	    .bindPopup("Cantidad de empresas: " + point.cantidad )
	    .addTo(map);
    }
}
