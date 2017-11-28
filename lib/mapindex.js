
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


var coor = [-23.64, -46.65]        
var m = L.map('map', {zoomControl:false}).setView(coor, 10);

var mq=L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {minZoom:2, attribution: '<a href="http://datadriven.yale.edu">Data Driven Yale</a> | <a href="socialconnectedness.org"> The Samuel Family Foundation</a>'});

mq.addTo(m);

new L.Control.Zoom({ position: 'topright' }).addTo(m);

/* ###########################################
######## INDICATOR LEGENDS ###################
########################################### */

// INCOME  
var incomelegend = L.control({position: 'bottomright'});
incomelegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
        grades_comma = ["0", "1,000", "2,000", "5,000", "10,000", "20,000", "50,000", "100,000"]
        labels = [];
    div.innerHTML += '<b> Income </b><br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorIncome(grades[i] + 1) + '"></i> ' +
            grades_comma[i] + (grades_comma[i + 1] ? '&ndash;' + grades_comma[i + 1] + '<br>' : '+');
    }
    return div;
};

incomelegend.addTo(m);

//UNEMPLOYED
var unemplegend = L.control({position: 'bottomright'});
unemplegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 5, 7.5, 10, 15, 20, 30, 40],
        labels = [];
    div.innerHTML += '<b> Unemployment (%)</b><br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorUnemp(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

//POVERTY
var povertylegend = L.control({position: 'bottomright'});
povertylegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 5, 7.5, 10, 15, 20, 30, 40],
        labels = [];
    div.innerHTML += '<b> Poverty (%)</b><br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorUnemp(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

//POPULATION
var populationlegend = L.control({position: 'bottomright'});
populationlegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 500, 5000, 10000, 25000, 50000, 100000, 250000],
        grades_comma = ["0", "500", "5,000", "10,000", "25,0000", "50,000", "100,000", "250,000"]
        labels = [];
    div.innerHTML += '<b> Population </b><br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorPop(grades[i] + 1) + '"></i> ' +
            grades_comma[i] + (grades_comma[i + 1] ? '&ndash;' + grades_comma[i + 1] + '<br>' : '+');
    }
    return div;
};

//UHI LEGEND
var uhilegend = L.control({position: 'bottomright'});
uhilegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 2, 4, 6, 8, 10, 12, 14],
        labels = [];
    div.innerHTML += '<b> Urban Heat Island (&degC)</b><br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorUHI(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

//TREE LEGEND
var treelegend = L.control({position: 'bottomright'});
treelegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 0.005, 0.010, 0.02, 0.05, 0.10, 0.15],
        labels = [];
    div.innerHTML += '<b> Tree Loss</b><br> Proportion of tree cover loss <br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorTree(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};


//AIRQ LEGEND
var airlegend = L.control({position: 'bottomright'});
airlegend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 30000, 60000, 90000, 120000, 250000, 400000],
        grades_comma = ["0", "30,0000", "60,000", "90,000", "120,000", "250,000", "400,000"],
        labels = [];
    div.innerHTML += '<b> Air Quality </b><br> ug/m3 PM 2.5 * population <br>'
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorAir(grades[i] + 1) + '"></i> ' +
            grades_comma[i] + (grades_comma[i + 1] ? '&ndash;' + grades_comma[i + 1] + '<br>' : '+');
    }
    return div;
};




/* ######################################
######### MAP WINDOW CHANGES ############
###################################### */

//Changes map view based upon option value selection in the drop down box above

window.amsterdam = function(){m.setView([52.365, 4.86],11)};
window.bangalore = function(){m.setView([12.98, 77.5],11)};
window.bangkok = function(){m.setView([13.75, 100.5],11)};
window.beijing = function(){m.setView([40.1, 116.35],9)};
window.berlin = function(){m.setView([52.52, 13.36],11)};
window.casablanca = function(){m.setView([33.58, -7.6],12)};
window.delhi = function(){m.setView([28.6, 77.2],10)};
window.hochiminh = function(){m.setView([10.77, 106.5],10)};
window.johannesburg = function(){ m.setView([-26.2, 28.03],10)};
window.losangeles = function(){m.setView([34.06, -118.32],10)};
window.london = function(){m.setView([51.51, -0.13],10)};
window.manila = function(){m.setView([14.562, 120.98],11)};
window.mexico = function(){m.setView([19.43, -99.13],11)};
window.newyork = function(){m.setView([40.76, -73.99],11)};
window.paris = function(){m.setView([48.86, 2.4],12)};
window.saopaulo = function(){m.setView([-23.64, -46.65],10)};
window.seoul = function(){m.setView([37.54, 126.98],11)};
window.singapore = function(){m.setView([1.32, 103.86],11)};
window.tokyo = function(){m.setView([35.69, 139.74],11)};
window.vancouver = function(){m.setView([49.25, -123.10],11)};


/* ###############################
####### COLOR TEMPLATES ##########
################################## */

function getColorUnemp(d) {
    return d > 30 ? '#7a0177' :
           d > 20  ? '#ae017e' :
           d > 15  ? '#dd3497' :
           d > 10  ? '#f768a1' :
           d > 8   ? '#fa9fb5' :
           d > 5   ? '#fcc5c0' :
           d > 3   ? '#fde0dd' :
           d > 0    ? '#fff7f3' :
           d < 0      ? '#B8B7B7' :
                      '#fff7fb';
}


//chloropleth coloring for income
function getColorIncome(d) {
    return d > 60000 ? '#800026' :
           d > 30000  ? '#BD0026' :
           d > 15000  ? '#E31A1C' :
           d > 7500  ? '#FC4E2A' :
           d > 5000   ? '#FD8D3C' :
           d > 2500   ? '#FEB24C' :
           d > 1000   ? '#FED976' :
           d < 1      ? '#B8B7B7' :
                      '#FFEDA0';
}

function getColorPop(d) {
    return d > 100000 ? '#016450' :
           d > 50000  ? '#02818a' :
           d > 25000  ? '#3690c0' :
           d > 1000  ? '#67a9cf' :
           d > 5000   ? '#a6bddb' :
           d > 2500   ? '#d0d1e6' :
           d > 1000   ? '#ece2f0' :
           d > 100    ? '#ece2f0' :
           d < 1      ? '#B8B7B7' :
                      '#fff7fb';
}

function getColorPov(d) {
    return d > 40 ? '#016450' :
           d > 30  ? '#02818a' :
           d > 20  ? '#3690c0' :
           d > 15  ? '#67a9cf' :
           d > 10   ? '#a6bddb' :
           d > 5   ? '#d0d1e6' :
           d > 2.5   ? '#ece2f0' :
           d > 0    ? '#ece2f0' :
           d < 0      ? '#B8B7B7' :
                      '#fff7fb';
}

function getColorUHI(d) {
    return d > 14 ? '#67001f' :
           d > 12  ? '#980043' :
           d > 10  ? '#ce1256' :
           d > 8  ? '#e7298a' :
           d > 6   ? '#df65b0' :
           d > 4   ? '#c994c7' :
           d > 2   ? '#d4b9da' :
           d > 0    ? '#e7e1ef' :
           d < 0      ? '#f7f4f9' :
                      '#fff7fb';
}

function getColorTree(d) {
    return d > 0.20 ? '#016450' :
           d > 0.15  ? '#02818a' :
           d > 0.10  ? '#3690c0' :
           d > 0.05 ? '#67a9cf' :
           d > 0.025   ? '#a6bddb' :
           d > 0.01   ? '#d0d1e6' :
           d > 0.005   ? '#ece2f0' :
           d > 0    ? '#ece2f0' :
           d < 0      ? '#B8B7B7' :
                      '#fff7fb';
}


function getColorAir(d) {
    return d > 500000 ? '#252525' :
           d > 350000  ? '#525252' :
           d > 250000  ? '#737373' :
           d > 150000  ? '#969696' :
           d > 90000   ? '#bdbdbd' :
           d > 60000   ? '#d9d9d9' :
           d > 30000   ? '#f0f0f0' :
           d > 0    ? '#ffffff' :
           d < 0      ? '#B8B7B7' :
                      '#fff7fb';
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

function povertystyle(feature) {
    return {
        fillColor: getColorPov(feature.properties.poverty),
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

//UHI styling
function UrbanHeatIslandstyle(feature) {
    return {
        fillColor: getColorUHI(feature.properties.dUHI_AQUA_m),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

//Treecover styling
function TreeCoverstyle(feature) {
    return {
        fillColor: getColorTree(feature.properties.Treecover_LossRatio),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

//Air quality styling
function AirQualitystyle(feature) {
    return {
        fillColor: getColorAir(feature.properties.aexp_average),
        weight: 1,
        opacity: 1,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7
    }
};

/* ######################################
######## CLICK EVENTS FOR STYLING #######
###################################### */

unempstyle = function(feature){
    all.setStyle(unemployedstyle);
    m.removeControl(incomelegend);
    m.removeControl(povertylegend);
    m.removeControl(populationlegend);
    m.removeControl(uhilegend);
    m.removeControl(treelegend);
    m.removeControl(airlegend);
    unemplegend.addTo(m);
}

incstyle = function(feature){
    all.setStyle(incomestyle);
    m.removeControl(unemplegend);
    m.removeControl(povertylegend);
    m.removeControl(populationlegend);
    m.removeControl(uhilegend);
    m.removeControl(treelegend);
    m.removeControl(airlegend);
    incomelegend.addTo(m);
    //legend_all.hide()
    
}

povstyle = function(feature){
    all.setStyle(povertystyle);
    m.removeControl(incomelegend);
    m.removeControl(unemplegend);
    m.removeControl(uhilegend);
    m.removeControl(populationlegend);
    m.removeControl(treelegend);
    m.removeControl(airlegend);
    povertylegend.addTo(m);    
}

uhistyle = function(feature){
    all.setStyle(UrbanHeatIslandstyle)
    m.removeControl(incomelegend);
    m.removeControl(unemplegend);
    m.removeControl(povertylegend);
    m.removeControl(populationlegend);
    m.removeControl(treelegend);
    m.removeControl(airlegend);
    uhilegend.addTo(m);
};

treestyle = function(feature){
    all.setStyle(TreeCoverstyle)
    m.removeControl(incomelegend);
    m.removeControl(unemplegend);
    m.removeControl(povertylegend);
    m.removeControl(populationlegend);
    m.removeControl(uhilegend);
    m.removeControl(airlegend);
    treelegend.addTo(m);
};

popstyle = function(feature){
    all.setStyle(populationstyle)
    m.removeControl(incomelegend);
    m.removeControl(unemplegend);
    m.removeControl(povertylegend);
    m.removeControl(uhilegend);
    m.removeControl(treelegend);
    m.removeControl(airlegend);
    populationlegend.addTo(m);
};

airstyle = function(feature){
    all.setStyle(AirQualitystyle)
    m.removeControl(incomelegend);
    m.removeControl(unemplegend);
    m.removeControl(povertylegend);
    m.removeControl(populationlegend);
    m.removeControl(uhilegend);
    m.removeControl(treelegend);
    airlegend.addTo(m);
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
        var czoom = m.getZoom();
        m.setZoom(czoom-3);
        var f = document.getElementById("loc");
        f.value = layer;
        console.log(f.value);
        m.closePopup();
    }
}

/* ###############################
####### ON EACH LAYER  ###########
################################## */

//creates a pop up layer showing name, income, and population
//tells the geojson to highlight upon mouse over
function onEachFeature(feature, layer) {
  pzoom = m.getZoom();
  layer.bindPopup("Name: " + feature.properties.nbhd + "<br> Income: " + feature.properties.income + "<br> Population: " + feature.properties.population + "<br> Poverty: " + feature.properties.poverty + "<br> Unemployment: " + feature.properties.unemp +  "<br> UHI: " + feature.properties.dUHI_AQUA_m + "<br> Tree Cover: " + feature.properties.Treecover_LossRatio + "<br> Air Quality: " + feature.properties.aexp_average);
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
  "includes/casablanca.geojson", "includes/johannesburg.geojson", "includes/bangkok.geojson", "includes/la_reduced.geojson", "includes/london.geojson"], 
  {style: incomestyle, onEachFeature:onEachFeature}).addTo(m)

/* #############################################
#### SEARCH PORTAL - CURRENTLY NOT IN USE ######
############################################# */

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