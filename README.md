# demography-based-service-area

# Overview

This ArcPython toolbox calculates the demographically weighted service area for a given input of facility locations. It requires the Network Anaalyst and Spatial Analyst ArcGIS extensions. 

## Inputs

![required inputs](https://github.com/JohnMBrandt/demography-based-service-area/blob/master/screenshots/Figure_1.png?raw=true)

* Network layer of roads
* Feature class containing point location of facilities
* Service area radius (time or miles)
* Census block group shapefile

## Operation

The workflow is as follows:

* Calculate service area using network analysis and a given distance threshold
* Dissolve service area borders within each census block group
* Calculate intersection between service area and census layer
* Calculate area of dissolved polygons within each census polygon
* Join area of dissolved polygons to census layer
* Calculate percent coverage of each census block group
* Extrapolate percent coverage to percent of demographic group served
* Optionally, extrapolate to larger census group

![alt text](http://url/to/img.png)

# Example results

![Example output](https://github.com/JohnMBrandt/demography-based-service-area/blob/master/screenshots/Rplot.png?raw=true)
