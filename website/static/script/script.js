document.addEventListener('DOMContentLoaded', function () {
    // Initialize the map
    const map = L.map('map').setView([10.867767741138728, 106.79413940560535], 18); // Đặt mức thu phóng ban đầu cao hơn

    // Base layers
    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 21,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    const satellite = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=YOUR_MAPBOX_ACCESS_TOKEN', {
        maxZoom: 21,
        attribution: '&copy; <a href="https://www.mapbox.com/about/maps/">Mapbox</a> contributors'
    });

    // Overlay layers
    const markersLayer = L.layerGroup();

    // Add base layers and overlays to the map
    const baseLayers = {
        "OpenStreetMap": osm,
        "Satellite": satellite
    };

    const overlays = {
        "Markers": markersLayer
    };

    L.control.layers(baseLayers, overlays).addTo(map);

    // Add default layers to the map
    osm.addTo(map);
    markersLayer.addTo(map);

    // Function to add markers to the markersLayer
    function addMarkers(markers) {
        markers.forEach(marker => {
            L.marker([marker.Latitude, marker.Longitude]).addTo(markersLayer)
                .bindPopup(`ReportID: ${marker.ReportID}, Device Name: ${marker.Device_Name}, Time Receive: ${marker.Time_Recieve}, Signal Strength: ${marker.Signal_Strength}`);
        });
    }

    // Event listener for form submission
    document.getElementById('deviceForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const date = document.getElementById('date').value;
        const deviceID = document.getElementById('deviceID').value;

        // Fetch data from backend
        fetch(`/submit?date=${date}&deviceID=${deviceID}`)
            .then(response => response.json())
            .then(data => {
                // Clear existing markers on the markersLayer
                markersLayer.clearLayers();
                // Add markers from received data
                addMarkers(data.markers);
                // Move the map to the position of the first marker
                const firstMarker = data.markers[0];
                map.setView([firstMarker.Latitude, firstMarker.Longitude], 18);
            })
            .catch(error => console.error('Error:', error));
    });
});
