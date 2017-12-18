'''
---------------------------------------------------------------------------------------------------------
| Part 2 of 3 of the census-based service area calculator.                                              |
| To use this toolkit, you will need a network layer of roads, a feature class of facility locations,   |
| census block level demographic data, and a shapefile of the counties encompassing the facilities.     |
|                                                                                                       |
| This script takes the following inputs:                                                               |
|                                                                                                       |
| input_shapefile  = output of Part 1, a shapefile containing areas of service area by census block     |
| service_area     = field within input_shapefile containing area of service polygon                    |
| census_area      = field within input_shapefile containing area of census polygon                     |
|                                                                                                       |
| output_field     = field to be calculated within output_shapefile containing percent coverage         |
| output_shapefile = location of output shapefile                                                       |
|                                                                                                       |
---------------------------------------------------------------------------------------------------------
'''

# Import packages
import sys, math, string, arcpy, os, traceback

arcpy.env.overwriteOutput = True

try:

    # Set input variables
    input_shapefile = arcpy.GetParameterAsText(0)   
    service_area = arcpy.GetParameterAsText(1)
    census_area = arcpy.GetParameterAsText(2)

    arcpy.AddMessage('\n' + "The input shapefile is" + input_shapefile + ", and"
        + service_area +  " and " + census_area + "are the input fields.")
    
    # Set output variables
    output_field = arcpy.GetParameterAsText(3)
    output_shapefile = arcpy.GetParameterAsText(4)

    arcpy.AddMessage("The name of the field to be added is " + output_field + "\n")
    arcpy.AddMessage('\n' + "The output shapefile is" + output_shapefile)

    # Create a new copy of the shapefile and save it as the output shapefile
    arcpy.Copy_management(input_shapefile, output_shapefile)
    arcpy.AddMessage('\n' + "Copied")

    # Add a new field to the output shapefile
    arcpy.AddField_management(output_shapefile, output_field, "DOUBLE", 20, 5)
    arcpy.AddMessage('\n' + "New Field Added")

    # Create a list of iterable records within the output shapefile
    ShpRecords = arcpy.UpdateCursor(output_shapefile)
    arcpy.AddMessage('\n' + "List made")


    # Generate variable that contains the name of the column containing shape data
    shapefield = arcpy.Describe(output_shapefile).shapeFieldName

    # Iterate over each index in the shapefile
    for record in ShpRecords:

        # Get the value of the data in the relevant fields
        service_value = record.getValue(service_area)
        census_value = record.getValue(census_area)

        # Calculate the percent coverage
        result = service_value/census_value

        # Save calculated data
        record.setValue(output_field, result)
        ShpRecords.updateRow(record)

    # Delete extraneous temp files
    del ShpRecords
    del record


except Exception as e:
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    exceptionreport = sys.exc_info()[2]
    arcpy.AddError("at this location: \n\n" + traceback.format_tb(exceptionreport)[0]+ "\n")
