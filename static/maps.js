// Инициализация карты
var map = L.map('map').setView([55.7558, 37.6173], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);
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
    createContextMenu(layer);

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

var markers = L.markerClusterGroup({
    disableClusteringAtZoom: 16,
    chunkedLoading: true,
    chunkProgress: updateProgressBar
});

var selectedObjects = [];
var polygons = [];

function exportToXLSX() {
    if (selectedObjects.length === 0) {
        alert('Пожалуйста, выберите хотя бы один объект для экспорта.');
        return;
    }

    var selectedData = selectedObjects.map(obj => {
        return {
            gid: obj.feature.properties.gid,
            map_name: obj.feature.properties.map_name // Assuming map_name is stored in feature properties
        };
    });

    fetch('/export/xlsx', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedData )
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'exported_data.xlsx');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    })
    .catch(error => {
        alert('Ошибка при экспорте данных в Excel: ' + error);
    });
}

function exportToSHP() {
    if (selectedObjects.length === 0) {
        alert('Пожалуйста, выберите хотя бы один объект для экспорта.');
        return;
    }

    var selectedData = selectedObjects.map(obj => {
        return {
            gid: obj.feature.properties.gid,
            map_name: obj.feature.properties.map_name
        };
    });

    fetch('/export/shp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedData )
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'exported_data.zip');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    })
    .catch(error => {
        alert('Ошибка при экспорте данных в SHP: ' + error);
    });
}

function loadMarkers(data) {
    markers.clearLayers();
    polygons.forEach(function(polygon) {
        map.removeLayer(polygon.layer);
    });
    polygons = [];

    var disableClusteringAtZoom = 12
    if (data.length > 1000) {
        disableClusteringAtZoom = 16
    }

    markers.options.disableClusteringAtZoom = disableClusteringAtZoom

    data.forEach(function(item) {
        var geoJsonFeature = {
            "type": "Feature",
            "properties": {
                "popupContent": item.popup + `<br><button onclick="openPanorama(${item.lat}, ${item.lon})">Просмотр панорамы</button>`,
                "gid": item.gid,
                "map_name": item.map_name
            },
            "geometry": JSON.parse(item.geom)
        };

        var polygonLayer = L.geoJSON(geoJsonFeature, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.popupContent);
                layer.on('contextmenu', function(e) {
                    handleMarkerRightClick(e, layer);
                });
            },
            style: {
                color: 'blue'  // Начальный цвет объектов
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

        setTimeout(function() {
            map.setView(singleFeatureBounds.getCenter(), map.getMaxZoom());
        }, 500);
    }
}

function updatePolygons() {
    var currentZoom = map.getZoom();
    var mapBounds = map.getBounds();

    polygons.forEach(function(polygon) {
        if (currentZoom >= markers.options.disableClusteringAtZoom && mapBounds.intersects(polygon.bounds)) {
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

function handleMarkerRightClick(e, layer) {
    var feature = layer.feature;  // Получаем feature из layer
    if (!feature || !feature.properties) {
        console.error('Feature or properties not found in the layer.');
        return;
    }
    var gid = feature.properties.gid;
    var index = selectedObjects.findIndex(obj => obj.feature.properties.gid === gid);
    if (index === -1) {
        selectedObjects.push({ layer: layer, feature: feature });
        layer.setStyle({ color: 'red' });  // Меняем цвет объекта на синий при добавлении
    } else {
        selectedObjects.splice(index, 1);
        layer.setStyle({ color: 'blue' });  // Возвращаем исходный цвет объекта при удалении
    }
    updateSelectedList();
}

function updateSelectedList() {
    var list = $('#selected-list');
    list.empty();
    selectedObjects.forEach(function(obj) {
        var listItem = $('<li>').text(obj.feature.properties.name || obj.feature.properties.address || 'Без названия');
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
    var selectedMaps = [];
    $('#map-select .dropdown-menu input:checked').each(function() {
        selectedMaps.push($(this).val());
    });
    if (!selectedMaps || selectedMaps.length === 0) return;


    $.post('/map', { maps: JSON.stringify(selectedMaps) }, function(data) {
        loadMarkers(data);
        loadColumns(selectedMaps[0])
    }, 'json');

}

function viewLongNarrowLayers(){
    var selectedMaps = [];
    $('#map-select .dropdown-menu input:checked').each(function() {
        selectedMaps.push($(this).val());
    });
    if (!selectedMaps || selectedMaps.length === 0) return;

    $.ajax({
        url: "/long_narrow_layers",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            maps: selectedMaps,
            threshold_ratio: 5.0
        }),
        dataType: "json",
        success: function(data) {
            loadMarkers(data);
            loadColumns(selectedMaps[0]);
        }
    });
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

    window.applyFilters = function() {
        const filters = {};
        $('#filter-select .filter-option input').each(function() {
            const column = $(this).attr('id');
            const value = $(this).val();
            console.log(`column = ${column}, value = ${value}`)
            if (value) {
                filters[column] = value;
            }
        });

        var selectedMaps = [];
        $('#map-select .dropdown-menu input:checked').each(function() {
            selectedMaps.push($(this).val());
        });
        if (!selectedMaps || selectedMaps.length === 0) return;

        let data = {
            filters: filters,
            class_name: selectedMaps[0]
        }

        $.ajax({
            url: '/filters',
            method: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(data) {
                loadMarkers(data);
            }
        });
    }

    $.get('/map_list', function(data) {
        var mapSelect = $('#map-select .dropdown-menu');
        for (var i = 0; i < data.length; i++) {
            mapSelect.append(
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

function loadColumns(map) {
        $.ajax({
            url: `/map_columns/${map}`,
            method: 'GET',
            success: function(data) {
                const filterSelect = $('#filter-select');
                filterSelect.empty();
                data.forEach(function(column) {
                    filterSelect.append(`
                        <div class="filter-option">
                            <label for="${column}">${column}</label>
                            <input type="text" id="${column}" name="${column}">
                        </div>
                    `);
                });
            }
        });
    }

function createContextMenu(layer) {
    layer.on('contextmenu', function(e) {
        // Удаляем предыдущее контекстное меню, если оно существует
        var existingMenu = document.querySelector('.context-menu');
        if (existingMenu) {
            existingMenu.parentNode.removeChild(existingMenu);
        }

        var contextMenu = L.DomUtil.create('div', 'context-menu', document.body);
        contextMenu.style.position = 'absolute';
        contextMenu.style.left = e.originalEvent.pageX + 'px';
        contextMenu.style.top = e.originalEvent.pageY + 'px';
        contextMenu.style.backgroundColor = 'white';
        contextMenu.style.border = '1px solid black';
        contextMenu.style.padding = '5px';
        contextMenu.style.zIndex = 1000;

        var selectAllBtn = L.DomUtil.create('button', '', contextMenu);
        selectAllBtn.innerHTML = 'Выбрать всё';
        selectAllBtn.onclick = function() {
            selectAllIntersecting(layer);
            contextMenu.parentNode.removeChild(contextMenu);
        };

        var unselectAllBtn = L.DomUtil.create('button', '', contextMenu);
        unselectAllBtn.innerHTML = 'Открепить всё';
        unselectAllBtn.onclick = function() {
            unselectAllIntersecting(layer);
            contextMenu.parentNode.removeChild(contextMenu);
        };

        document.body.appendChild(contextMenu);

        // Удаляем контекстное меню при клике в любом другом месте
        document.addEventListener('click', function removeContextMenu(event) {
            if (!contextMenu.contains(event.target)) {
                if (contextMenu) {
                    contextMenu.parentNode.removeChild(contextMenu);
                    document.removeEventListener('click', removeContextMenu);
                }
            }
        });

        // Останавливаем распространение события клика по документу
        e.originalEvent.stopPropagation();
    });
}

function selectAllIntersecting(layer) {
    if (!drawnItems) {
        console.error('drawnItems is not defined');
        return;
    }

    polygons.forEach(function(polygonObj) {
        var drawnLayer = polygonObj.layer;
        if (drawnLayer !== layer && drawnLayer instanceof L.Polygon) {
            if (layer.getBounds().intersects(drawnLayer.getBounds())) {
                drawnLayer.setStyle({ color: 'red' });
                var feature = drawnLayer.feature;
                if (feature && feature.properties) {
                    var gid = feature.properties.gid;
                    var index = selectedObjects.findIndex(obj => obj.feature.properties.gid === gid);
                    if (index === -1) {
                        selectedObjects.push({ layer: drawnLayer, feature: feature });
                    }
                }
            }
        }
    });
    updateSelectedList();
}

function unselectAllIntersecting(layer) {
    if (!drawnItems) {
        console.error('drawnItems is not defined');
        return;
    }

    polygons.forEach(function(polygonObj) {
        var drawnLayer = polygonObj.layer;
        if (drawnLayer !== layer && drawnLayer instanceof L.Polygon) {
            if (layer.getBounds().intersects(drawnLayer.getBounds())) {
                drawnLayer.setStyle({ color: 'blue' });
                var feature = drawnLayer.feature;
                if (feature && feature.properties) {
                    var gid = feature.properties.gid;
                    var index = selectedObjects.findIndex(obj => obj.feature.properties.gid === gid);
                    if (index !== -1) {
                        selectedObjects.splice(index, 1);
                    }
                }
            }
        }
    });
    updateSelectedList();
}


function updateSelectedList() {
    var list = $('#selected-list');
    list.empty();
    selectedObjects.forEach(function(obj) {
        var listItem = $('<li>').text(obj.feature.properties.name || obj.feature.properties.address);
        list.append(listItem);
    });
}
