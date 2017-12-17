'''
This script takes the following inputs:

NetworkRoad       = a network layer
Facility          = a shapefile/feature class containing point locations of facilities
ServiceAreaRadius = how many miles to calculate service area
CensusLayer       = a polygon feature class/shapefile/geojson of census data (county/block)
DissolveField     = field, within the Census layer, that differentiates between polygons, preferably an FID

outLayerFile      = name of service area layer (.shp)
outputDissolved   = dissolved surface area layer (.shp)
outputJoined      = final output latyer (.shp)

The goal of the script is to:
    a) Calculate service area polygons for facilities
    b) Calculate area of resulting service area within each census polygon

This script can be combined with Brandt,John,09.py to calculate:
    a) the percentage of each census polygon with service to a facility
    b) the ranking of counties in the census feature class with regards to percent service coverage

'''

#Import system modules
import sys,os,shutil,arcpy,string,traceback
from arcpy import env
from arcpy.sa import *


try:
    # Check out the necessary extensions
    arcpy.CheckOutExtension("Network")
    arcpy.CheckOutExtension("Spatial")

    # Set environment & output settings
    env.workspace = "C:\Users\John\Desktop\GIS Final"
    env.overwriteOutput = True

    # Set input variables
    NetworkRoad = arcpy.GetParameterAsText(0)
    Facility = arcpy.GetParameterAsText(1)
    ServiceAreaRadius = arcpy.GetParameterAsText(2)
    CensusLayer = arcpy.GetParameterAsText(3)
    DissolveField = arcpy.GetParameterAsText(4)

    # Set output variables
    outLayerFile = arcpy.GetParameterAsText(5)
    outputDissolved = arcpy.GetParameterAsText(6)
    outputJoined = arcpy.GetParameterAsText(7)

    arcpy.AddMessage('\n' + "The network road input shapefile name is: " +NetworkRoad+'\n')


    # Build the network dataset
    arcpy.na.BuildNetwork(in_network_dataset=NetworkRoad)

    # Calculate locations of points within the network


    # Create a service area layer
    outLayerName = arcpy.na.MakeServiceAreaLayer(in_network_dataset=NetworkRoad,
                                impedance_attribute="Length",
                                travel_from_to="TRAVEL_FROM",
                                default_break_values="20000",
                                polygon_type="SIMPLE_POLYS",
                                merge="NO_MERGE",
                                nesting_type="RINGS",
                                line_type="NO_LINES",
                                overlap="OVERLAP",
                                split="NO_SPLIT",
                                excluded_source_name="", accumulate_attribute_name="",
                                UTurn_policy="ALLOW_UTURNS",
                                restriction_attribute_name="Oneway",
                                polygon_trim="TRIM_POLYS",
                                poly_trim_value="250 Meters",
                                lines_source_fields="NO_LINES_SOURCE_FIELDS",
                                hierarchy="NO_HIERARCHY", time_of_day="")


    # Get the output of the service layer
    FacilitiesInterim = outLayerName.getOutput(0)

    # Create a variable referencing the list of sublayers of the service area layer
    naClasses = arcpy.na.GetNAClassNames(FacilitiesInterim)

    # Create a variable storing the name of the sublayer containing the facilities
    FacilitiesLayer = arcpy.na.GetNAClassNames(FacilitiesInterim)["Facilities"]

    # Add the shapefile of locations to the service area layer
    arcpy.na.AddLocations(outLayerName, FacilitiesLayer, Facility, "", "")

    # Solve the service area
    arcpy.na.Solve(outLayerName)

    # Use arcpy mapping and the naClasses variable we defined above to create a variable
    # storing the polygons sublayer
    polygonsSubLayer = arcpy.mapping.ListLayers(FacilitiesInterim, naClasses["SAPolygons"])[0]

    # Copy the polygons sublayer to the disk, as a shapefile
    arcpy.CopyFeatures_management(polygonsSubLayer, outLayerFile)

    # Calculate the intersection between the service area and the census layer


    # Dissolve the borders between service areas within each census polygon
    dissolved = arcpy.Dissolve_management(in_features=outLayerFile,
                                       dissolve_field="FromBreak",
                                       statistics_fields="",
                                       multi_part="MULTI_PART",
                                       unsplit_lines="DISSOLVE_LINES")

    intersected = arcpy.Intersect_analysis([dissolved, CensusLayer],
                                           join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

    # Export the dissolved shapefile to the disk
    arcpy.CopyFeatures_management(dissolved, outputDissolved)

    # Calculate the area of the dissolved polygons within each census polygon
    intersected_area = arcpy.AddGeometryAttributes_management(Input_Features = intersected,
                                                        Geometry_Properties="AREA_GEODESIC",
                                                        Length_Unit="",
                                                        Area_Unit="SQUARE_MILES_US",
                                                        Coordinate_System="")

    Census_area = arcpy.AddGeometryAttributes_management(Input_Features = CensusLayer,
                                                        Geometry_Properties="AREA_GEODESIC",
                                                        Length_Unit="",
                                                        Area_Unit="SQUARE_MILES_US",
                                                        Coordinate_System="")

    # Join the layer containing the area of the dissolved polygons to the census layer
    arcpy.SpatialJoin_analysis(target_features=Census_area,
                        join_features=intersected_area,
                        out_feature_class = outputJoined,
                        join_operation="JOIN_ONE_TO_ONE",
                        join_type="KEEP_ALL",
                        match_option="CONTAINS",
                        search_radius="",
                        distance_field_name="")


    # When done, turn off the Spatial Analysis and Network Analysis Extensions
    arcpy.CheckInExtension("Network")
    arcpy.CheckInExtension("Spatial")


# If the above script fails, report an error
# - as adopted from Dana Tomlin's Resources for GSD -

except Exception as e:
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    exceptionreport = sys.exc_info()[2]
    arcpy.AddError("at this location: \n\n" + traceback.format_tb(exceptionreport)[0]+ "\n")