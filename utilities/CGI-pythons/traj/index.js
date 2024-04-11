(function (window) {
  'use strict';
  var L = window.L;

  function initMap() {
      var control;
      var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: 'Map data &copy; 2013 OpenStreetMap contributors'
      });
      var map = L.map('map', {
          center: [23.6, 120.9],
          zoom: 7
      }).addLayer(osm);
      var style = {
          color: 'blue',
          opacity: 0.5,
          fillOpacity: 0.3,
          weight: 1,
          clickable: false
      };
      L.Control.FileLayerLoad.LABEL = '<img class="icon" src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Gnome-folder.svg" alt="file icon"/>';
      control = L.Control.fileLayerLoad({
          fitBounds: true,
          layerOptions: {
              style: style,
              pointToLayer: function (data, latlng) {
                  return L.circleMarker(
                      latlng, {
                          style: style
                      }
                  );
              }
          }
      });
      control.addTo(map);
      control.loader.on('data:loaded', function (e) {
          var layer = e.layer;
          var kk = Object.keys(layer._layers);
          var i = kk[0];
          var lat0 = layer._layers[i]["_latlng"]["lat"];
          var lon0 = layer._layers[i]["_latlng"]["lng"];
          var ymd = layer._layers[i]["feature"]["properties"]["description"];
          console.log(layer._layers[i]["feature"], layer._layers[i]["_latlng"]);
          L.marker([lat0, lon0]).addTo(map)
              .bindPopup(ymd)
              .openPopup();
      });
  }

  window.addEventListener('load', function () {
      initMap();
  });
}(window));
