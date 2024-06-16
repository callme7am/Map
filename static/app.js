var map = L.map('map').setView([55.7558, 37.6173], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var markers = L.markerClusterGroup({
    disableClusteringAtZoom: 16,
    chunkedLoading: true,
    chunkProgress: updateProgressBar
});

var selectedObjects = [];

function exportToXLSX() {
    window.location.href = '/export/xlsx';
}

L.FeatureClusterable = L.FeatureGroup.extend({
    getLatLng: function() {
        if (this.getLayers().length > 0) {
            return this.getLayers()[0].getLatLng();
        }
        return null;
    },
    setLatLng: function(latlng) {
        this.eachLayer(function(layer) {
            if (layer.setLatLng) {
                layer.setLatLng(latlng);
            }
        });
    }
});

var polygons = [];

function loadMarkers(data) {
    markers.clearLayers();
    polygons.forEach(function(polygon) {
        map.removeLayer(polygon.layer);
    });
    polygons = [];

    data.forEach(function(item) {
        var geoJsonFeature = {
            "type": "Feature",
            "properties": {
                "popupContent": item.popup + `<br><button onclick="openPanorama(${item.lat}, ${item.lon})">Просмотр панорамы</button>`
            },
            "geometry": JSON.parse(item.geom)
        };

        var polygonLayer = L.geoJSON(geoJsonFeature, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.popupContent);
                layer.on('contextmenu', function(e) {
                    handleMarkerRightClick(e, item);
                });
            }
        });

        polygons.push({ layer: polygonLayer, bounds: polygonLayer.getBounds() });

        var center = polygonLayer.getBounds().getCenter();
        var emptyMarker = L.marker(center, {
            icon: L.divIcon({ html: '', className: 'dummy' })
        });

        markers.addLayer(emptyMarker);
    });

    map.addLayer(markers);
    updatePolygons();

    if (data.length === 1) {
        var singleFeatureBounds = polygons[0].bounds;
        map.fitBounds(singleFeatureBounds);

        // Устанавливаем максимальный уровень увеличения
        setTimeout(function() {
            map.setView(singleFeatureBounds.getCenter(), map.getMaxZoom());
        }, 500);
    }
}

function updatePolygons() {
    var currentZoom = map.getZoom();
    var mapBounds = map.getBounds();

    polygons.forEach(function(polygon) {
        if (currentZoom >= 16 && mapBounds.intersects(polygon.bounds)) {
            if (!map.hasLayer(polygon.layer)) {
                map.addLayer(polygon.layer);
            }
        } else {
            if (map.hasLayer(polygon.layer)) {
                map.removeLayer(polygon.layer);
            }
        }
    });
}

map.on('zoomend moveend', function() {
    updatePolygons();
});

markers.on('clusterclick', function (a) {
    a.layer.zoomToBounds();
});

function openPanorama(lat, lon) {
    var url = `https://yandex.ru/maps/?ll=${lon},${lat}&mode=poi&panorama%5Bdirection%5D=176.300000%2C10.000000&panorama%5Bfull%5D=true&panorama%5Bpoint%5D=${lon},${lat}&panorama%5Bspan%5D=113.544749%2C60.000000&poi%5Bpoint%5D=${lon},${lat}&z=14`;
    window.open(url, '_blank');
}

function handleMarkerRightClick(e, feature) {
    var gid = feature.properties.gid;
    var index = selectedObjects.findIndex(obj => obj.properties.gid === gid);
    if (index === -1) {
        selectedObjects.push(feature);
    } else {
        selectedObjects.splice(index, 1);
    }
    updateSelectedList();
}

function updateSelectedList() {
    var list = $('#selected-list');
    list.empty();
    selectedObjects.forEach(function(obj) {
        var listItem = $('<li>').text(obj.properties.name || obj.properties.address);
        list.append(listItem);
    });
}

function saveComment(event, gid) {
    event.preventDefault();
    var form = event.target;
    var comment = form.querySelector('textarea[name="comment"]').value;

    $.post('/comment/' + gid, { comment: comment }, function(data) {
        if (data.status === 'success') {
            alert(data.message);
            changeMap();
        } else {
            alert(data.message);
        }
    }, 'json');
}

function resetMarkers() {
    changeMap();
}

function changeMap() {
    var mapName = $('#map-select').val();
    $.get('/map/' + mapName, function(data) {
        loadMarkers(data);
    }, 'json');
}

function showIntersections() {
    var map1 = $('#map-select-1').val();
    var map2 = $('#map-select-2').val();
    $.post('/map_intersections', { maps: JSON.stringify([map1, map2]) }, function(data) {
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
    console.log(`elapsed ${elapsed}, processed ${processed}, total ${total}`);

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
    $('#search-form').submit(function(event) {
        event.preventDefault();
        var cadastra = $('#cadastra').val();
        $.post('/search', { cadastra: cadastra }, function(data) {
            loadMarkers(data);
        }, 'json');
    });


    $('#search-address-form').submit(function(event) {
        event.preventDefault();
        var address = $('#address').val();
        $.get('/search_by_address', { address: address }, function(data) {
            loadMarkers(data);
        }, 'json');
    });

    $.get('/map_list', function(data) {
        var mapSelect = $('#map-select');
        var mapSelect1 = $('#map-select-1');
        var mapSelect2 = $('#map-select-2');
        for (var i = 0; i < data.length; i++) {
            mapSelect.append(new Option(data[i], data[i]));
            mapSelect1.append(new Option(data[i], data[i]));
            mapSelect2.append(new Option(data[i], data[i]));
        }
        changeMap();
    });

    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems
        }
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function(event) {
        var layer = event.layer;
        drawnItems.addLayer(layer);

        if (layer instanceof L.Polygon) {
            var area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
            alert("Площадь: " + area.toFixed(2) + " кв.м");
        } else if (layer instanceof L.Polyline) {
            var length = 0;
            var latlngs = layer.getLatLngs();
            for (var i = 0; i < latlngs.length - 1; i++) {
                length += latlngs[i].distanceTo(latlngs[i + 1]);
            }
            alert("Длина: " + length.toFixed(2) + " м");
        }
    });
});
