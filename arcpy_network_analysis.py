'''
I am not using any raster files for my final project so I focused on my data instead. I was going to do both
but I ended up spending > 20 hours trying to get this script to work. Currently, the script should work, but 
I cannot get it to work with the data I'm using for my final project. Even after hours and hours of trying.



This script takes the following inputs:

NetworkRoad = a network layer
Facility = a shapefile/feature class containing point locations of facilities
ServiceAreaRadius = how many miles to calculate service area
CensusLayer = a polygon feature class/shapefile/geojson of census data (county/block)

outLayerName = name of service area layer (.lyr)
outputJoined = output layer (.shp)

The goal of the script is to:
	a) Calculate service area polygons for inputed facilities
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

	# Set input and output variables
	NetworkRoad = arcpy.GetParameterAsText(0)
	Facility = arcpy.GetParameterAsText(1)
	ServiceAreaRadius = arcpy.GetParameterAsText(2)
	CensusLayer = arcpy.GetParameterAsText(3)


	outLayerName = arcpy.GetParameterAsText(4)
	outputJoined = arcpy.GetParameterAsText(5)

	arcpy.AddMessage('\n' + "The network road input shapefile name is: " +NetworkRoad+'\n')


	# Build the network dataset
	arcpy.na.BuildNetwork(in_network_dataset=NetworkRoad)

	# Calculate locations of points within the network
	arcpy.na.CalculateLocations(in_point_features=Facility,
                            in_network_dataset=NetworkRoad,
                            search_tolerance="5000 Meters",
                            search_criteria="StreetSegment SHAPE;StreetSegment_ND_Junctions SHAPE",
                            match_type="MATCH_TO_CLOSEST",
                            source_ID_field="SourceID",
                            source_OID_field="SourceOID",
                            position_field="PosAlong",
                            side_field="SideOfEdge",
                            snap_X_field="SnapX",
                            snap_Y_field="SnapY",
                            distance_field="Distance",
                            snap_Z_field="",
                            location_field="",
                            exclude_restricted_elements="INCLUDE")

	# Service area calculation
	arcpy.na.MakeServiceAreaLayer(in_network_dataset=NetworkRoad,
                                out_network_analysis_layer = outLayerName,
                                impedance_attribute="Length",
                                travel_from_to="TRAVEL_FROM",
                                default_break_values="1 5 10 15 20 25 30",
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
                                poly_trim_value="100 Meters",
                                lines_source_fields="NO_LINES_SOURCE_FIELDS",
                                hierarchy="NO_HIERARCHY", time_of_day="")


	# Calculate the intersection between the service area and census layer
	intersected = arcpy.Intersect_analysis(
	    in_features="C:/Users/John/Desktop/GIS Final/"  + outLayerName + "/Polygons #;" + CensusLayer+ " #",
	    join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

	# Dissolve the borders between service areas within each census polygon
	dissolved = arcpy.Dissolve_management(in_features= intersected,
                                       dissolve_field="NAME_1",
                                       statistics_fields="",
                                       multi_part="MULTI_PART",
                                       unsplit_lines="DISSOLVE_LINES")
	
	# Calculate the area of the dissolved polygons within each census polygon
	dissolve_area = arcpy.AddGeometryAttributes_management(Input_Features = dissolved,
                                                        Geometry_Properties="AREA_GEODESIC",
                                                        Length_Unit="",
                                                        Area_Unit="SQUARE_MILES_US",
                                                        Coordinate_System="")

	# Join the layer containing the area of the dissolved polygons to the census layer
	arcpy.SpatialJoin_analysis(target_features=CensusLayer,
                        join_features=dissolve_area,
                        out_feature_class = outputJoined,
                        join_operation="JOIN_ONE_TO_ONE",
                        join_type="KEEP_ALL",
                        match_option="INTERSECT",
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