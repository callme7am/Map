var map = L.map('map').setView([55.7558, 37.6173], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var markers = L.markerClusterGroup({
    disableClusteringAtZoom: 16,
    chunkedLoading: true,
    chunkProgress: updateProgressBar
});

function showIntersections() {
    var selectedMaps = [];
    $('#map-select-1 .dropdown-menu input:checked').each(function() {
        selectedMaps.push($(this).val());
    });
    if (!selectedMaps || selectedMaps.length < 2) {
        alert('Пожалуйста, выберите как минимум две карты для пересечений.');
        return;
    }

    $.post('/map_intersections', { maps: JSON.stringify(selectedMaps) }, function(data) {
        var raw_polygons = data;

        markers.clearLayers();

        for (var i = 0; i < raw_polygons.length; i++) {
            var polygon = L.geoJSON(JSON.parse(raw_polygons[i]), {
                style: function() {
                    return { color: "red" };
                }
            });
            markers.addLayer(polygon);
        }

        map.addLayer(markers);
    }, 'json');
}

function updateProgressBar(processed, total, elapsed, layersArray) {
    var progress = document.getElementById('progress');
    var progressBar = document.getElementById('progress-bar');

    if (elapsed > 50) {
        progress.style.display = 'block';
        progressBar.style.width = Math.round(processed / total * 100) + '%';
    }
    if (processed === total) {
        progress.style.display = 'none';
    }
}

$(document).ready(function() {
    $.get('/map_list', function(data) {
        var mapSelect1 = $('#map-select-1 .dropdown-menu');
        for (var i = 0; i < data.length; i++) {
            mapSelect1.append(
                `<div class="form-check">
                    <input class="form-check-input" type="checkbox" value="${data[i]}" id="map-${i}">
                    <label class="form-check-label" for="map-${i}">
                        ${data[i]}
                    </label>
                </div>`
            );
        }
    });
});
