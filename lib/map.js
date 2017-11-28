
/* ########################################
####### FUNCTIONALITY FOR NAVBAR ##########
######################################## */

function applyMargins() {
  var leftToggler = $(".mini-submenu-left");
    if (leftToggler.is(":visible")) {
      $("#map .ol-zoom")
        .css("margin-left", 0)
        .removeClass("zoom-top-opened-sidebar")
        .addClass("zoom-top-collapsed");
    } else {
      $("#map .ol-zoom")
        .css("margin-left", $(".sidebar-left").width())
        .removeClass("zoom-top-opened-sidebar")
        .removeClass("zoom-top-collapsed");
    }
}

function isConstrained() {
  return $(".sidebar").width() == $(window).width();
}
function applyInitialUIState() {
  if (isConstrained()) {
    $(".sidebar-left .sidebar-body").fadeOut('slide');
    $('.mini-submenu-left').fadeIn();
  }
}

$(function(){
  $('.sidebar-left .slide-submenu').on('click',function() {
    var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide',function(){
        $('.mini-submenu-left').fadeIn();
          applyMargins();
      });
  });
  $('.mini-submenu-left').on('click',function() {
    var thisEl = $(this);
      $('.sidebar-left .sidebar-body').toggle('slide');
        thisEl.hide();
        applyMargins();
  });
$(window).on("resize", applyMargins);




/* ####################################
####### BEGIN MAP JAVASCRIPT ##########
####################################### */


var coor = [52.365, 4.86]
var m= L.map('map').setView(coor, 11);
var m1= L.map('map1').setView(coor, 11);

L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
  minZoom:2,
  attribution: '<a href="http://datadriven.yale.edu">Data Driven Yale</a>'
}).addTo(m)

L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
  minZoom:2,
  attribution: '<a href="http://datadriven.yale.edu">Data Driven Yale</a>'
}).addTo(m1)

//Changes map view based upon option value selection in the drop down box above

sv = function(l, z) {
  m.setView(l,z)
  m1.setView(l,z)
}

window.amsterdam = function(){sv([52.365, 4.86],11)};
window.bangalore = function(){sv([12.98, 77.5],11)};
window.bangkok = function(){sv([13.75, 100.5],11)};
window.beijing = function(){sv([40.1, 116.35],9)};
window.berlin = function(){sv([52.52, 13.36],11)};
window.casablanca = function(){sv([33.58, -7.6],12)};
window.delhi = function(){sv([28.6, 77.2],10)};
window.hochiminh = function(){sv([10.77, 106.5],10)};
window.johannesburg = function(){sv([-26.2, 28.03],10)};
window.losangeles = function(){sv([34.06, -118.32],10)};
window.london = function(){sv([51.51, -0.13],10)};
window.manila = function(){sv([14.562, 120.98],11)};
window.mexico = function(){sv([19.43, -99.13],11)};
window.newyork = function(){sv([40.76, -73.99],11)};
window.paris = function(){sv([48.86, 2.4],12)};
window.saopaulo = function(){sv([-23.55, -46.65],11)};
window.seoul = function(){sv([37.54, 126.98],11)};
window.singapore = function(){sv([1.32, 103.86],11)};
window.tokyo = function(){sv([35.69, 139.74],11)};
window.vancouver = function(){sv([49.25, -123.10],11)};



/*

ALSO DEFUNCT

//Layer selector
//Income or Population
var legend2 = L.control({position: 'topright'});
legend2.onAdd = function (m) {
    var div2 = L.DomUtil.create('div', 'dropdown');
    div2.innerHTML = '<select id="styling" onchange="allstyle()"><option value = income>Income</option><option value=population>Population</option></select>';
    div2.firstChild.onmousedown = div2.firstChild.ondblclick = L.DomEvent.stopPropagation;
    return div2;
};
legend2.addTo(m);

*/


/* ###############################
####### COLOR TEMPLATES ##########
################################## */

function getColorUnemp(d) {
    return d > 30  ? '#7a0177' :
           d > 20  ? '#ae017e' :
           d > 15  ? '#dd3497' :
           d > 10  ? '#f768a1' :
           d > 8   ? '#fa9fb5' :
           d > 5   ? '#fcc5c0' :
           d > 3   ? '#fde0dd' :
           d > 0   ? '#fff7f3' :
           d < 0   ? '#B8B7B7' :
                     '#fff7fb' ;
}


//chloropleth coloring for income
function getColorIncome(d) {
    return d > 60000  ? '#800026' :
           d > 30000  ? '#BD0026' :
           d > 15000  ? '#E31A1C' :
           d > 7500   ? '#FC4E2A' :
           d > 5000   ? '#FD8D3C' :
           d > 2500   ? '#FEB24C' :
           d > 1000   ? '#FED976' :
           d < 1      ? '#B8B7B7' :
                        '#FFEDA0' ;
}

function getColorPop(d) {
    return d > 100000 ? '#016450' :
           d > 50000  ? '#02818a' :
           d > 25000  ? '#3690c0' :
           d > 1000   ? '#67a9cf' :
           d > 5000   ? '#a6bddb' :
           d > 2500   ? '#d0d1e6' :
           d > 1000   ? '#ece2f0' :
           d > 100    ? '#ece2f0' :
           d < 1      ? '#B8B7B7' :
                        '#fff7fb' ;
}

/* ###############################
####### LAYER STYLING ############
################################## */

//population styling
function populationstyle(feature) {
    return {
        fillColor: getColorPop(feature.properties.population),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

//unemployed styling
function unemployedstyle(feature) {
    return {
        fillColor: getColorUnemp(feature.properties.unemp),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

//income styling
function incomestyle(feature) {
    return {
        fillColor: getColorIncome(feature.properties.income),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

unempstyle = function(feature){
    all.setStyle(unemployedstyle)
}

incstyle = function(feature){
    all.setStyle(incomestyle)
}


popstyle = function(feature){
    all.setStyle(populationstyle)
};


/* ###############################
####### MOUSE EVENTS #############
################################## */


//Highlight on mouse over
function highlightFeature(e) {
  var layer = e.target;
    layer.setStyle({
      weight: 5,
      color: 'white',
      dashArray: '',
      fillOpacity: 0.2
  });
  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    layer.bringToFront();
  }
}

//Remove highlight on mouse leave

function resetHighlight(e) {
  var layer = e.target;
  layer.setStyle({
    weight: 1,
    color: 'black',
    dashArray: '',
    opacity: 1,
    fillOpacity: 0.7
  });
}

//Zoom to feature upon clicking on it if user is zoomed out to see the whole world
function zoomToFeature(feature, layer) {
    pzoom = m.getZoom();
    if (pzoom < 6){
        m.fitBounds(feature.target.getBounds());
        m1.fitBounds(feature.target.getBounds());
        var czoom = m.getZoom();
        m.setZoom(czoom-3);
        m1.setZoom(czoom-3);
        var f = document.getElementById("loc");
        f.value = layer;
        console.log(f.value);
        m.closePopup();
        m1.closePopup();
    }
}

// sets the map that sends center and zoom data to the other.
// prevents odd feedback loops where both maps change each other.

var active_map = undefined;

m.on('mousedown', function(e) {
  active_map = 'm';
});

m1.on('mousedown', function(e) {
  active_map = 'm1';
});

// sets m1 location to m location when m is the active map

m.on('move', function(e) {
  if (active_map == 'm') {
    m1.setView(m.getCenter(), m.getZoom());
  }
});

// sets m location to m1 location when m1 is the active map

m1.on('move', function(e) {
  if (active_map == 'm1') {
    m.setView(m1.getCenter(), m1.getZoom());
  }
});

// syncs zoom levels. Doesn't need active map since zoom is slower 

m.on('zoom', function(e) {
  m1.setView(m.getCenter(), m.getZoom());
});

m1.on('zoom', function(e) {
  m.setView(m1.getCenter(), m1.getZoom());
});


/* ###############################
####### ON EACH LAYER  ###########
################################## */

//creates a pop up layer showing name, income, and population
//tells the geojson to highlight upon mouse over
function onEachFeature(feature, layer) {
  pzoom = m.getZoom();
  layer.bindPopup("Name: " + feature.properties.nbhd + "<br> Income: " + feature.properties.income + "<br> Population: " + feature.properties.population + "<br> Unemployment: " + feature.properties.unemp + "%");
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: zoomToFeature
  });
}


/* ###############################
####### ADD GEOJSONS #############
################################## */

var all = new L.GeoJSON.AJAX(["includes/amsterdam2.geojson", "includes/bangalore.geojson", "includes/ny_reduced.geojson",
  "includes/paris.geojson", "includes/saopaulo.geojson", "includes/seoul.geojson", "includes/singapore.geojson", "includes/vancouver.geojson", "includes/tokyo.geojson",
  "includes/delhi.geojson", "includes/mexico.geojson", "includes/hochiminh.geojson", "includes/manila.geojson", "includes/beijing.geojson", "includes/berlin.geojson",
  "includes/casablanca.geojson", "includes/johannesburg.geojson", "includes/bangkok_red.geojson", "includes/la_reduced.geojson", "includes/london.geojson"],
  {style: incomestyle, onEachFeature:onEachFeature}).addTo(m);

var all = new L.GeoJSON.AJAX(["includes/amsterdam2.geojson", "includes/bangalore.geojson", "includes/ny_reduced.geojson",
  "includes/paris.geojson", "includes/saopaulo.geojson", "includes/seoul.geojson", "includes/singapore.geojson", "includes/vancouver.geojson", "includes/tokyo.geojson",
  "includes/delhi.geojson", "includes/mexico.geojson", "includes/hochiminh.geojson", "includes/manila.geojson", "includes/beijing.geojson", "includes/berlin.geojson",
  "includes/casablanca.geojson", "includes/johannesburg.geojson", "includes/bangkok_red.geojson", "includes/la_reduced.geojson", "includes/london.geojson"],
  {style: incomestyle, onEachFeature:onEachFeature}).addTo(m1);

/* DEFUNCT

allstyle = function(feature){
    var e = document.getElementById("styling");
    //Get value of index
    var v = e.value;
    if (v == "population"){
        all.setStyle(populationstyle)
    }
    else if (v == "income"){
        all.setStyle(incomestyle)
    }
}

*/

//Next 5 lines are the search control
var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
var provider = new OpenStreetMapProvider();
var searchControl = new GeoSearchControl({provider: provider,});
m.addControl(searchControl);

  applyInitialUIState();
  applyMargins();
});

$(document).ready(function () {

    $('#PageModal').modal('show');

});
