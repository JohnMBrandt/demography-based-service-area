'''
---------------------------------------------------------------------------------------------------------
| Part 3 of 3 of the census-based service area calculator.                                              |
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



import sys, math, string, arcpy, os, traceback

arcpy.env.overwriteOutput = True

try:


    # Set input variables
    input_part_2 = arcpy.GetParameterAsText(0) # input shapefile
    input_census_file = arcpy.GetParameterAsText(1) # input census file
    arcpy.AddMessage('\n' + "The input shapefiles are" + input_part_2 + input_census_file)

    # User input of field to be normalized by area
    percent_coverage = arcpy.GetParameterAsText(2) # percent coverage

    perc_calc = arcpy.GetParameterAsText(3) #output - service area % * census value
    total_regions    = arcpy.GetParameterAsText(4) # census input data

    dissolve_field   = arcpy.GetParameterAsText(5) # county FID

    # User input of field to contain the calculated data
    OutputField      = arcpy.GetParameterAsText(6)
    arcpy.AddMessage("The name of the field to be added is " + OutputField + "\n")

    # User input of location to save output shapefile
    OutputShapeFile  = arcpy.GetParameterAsText(7)
    arcpy.AddMessage('\n' + "The output shapefile is" + OutputShapeFile)


    arcpy.AddField_management(input_part_2, perc_calc, "DOUBLE", 20, 5)

    ShpRecords_calc_number = arcpy.UpdateCursor(input_part_2)

    for record in ShpRecords_calc_number:
        census_value = record.getValue(total_regions)
        percent_coverage_value = record.getValue(percent_coverage)
        result = census_value * percent_coverage_value
        record.setValue(perc_calc, result)
        ShpRecords_calc_number.updateRow(record)

    del ShpRecords_calc_number
    del record

    outPutIntersect = arcpy.Intersect_analysis([input_part_2, input_census_file],
                             join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

    dissolved = arcpy.Dissolve_management(in_features=outPutIntersect,
                              out_feature_class=OutputShapeFile,
                              dissolve_field=dissolve_field, statistics_fields=total_regions + " SUM;" + perc_calc + " SUM",
                              multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")



    arcpy.AddField_management(OutputShapeFile, OutputField, "DOUBLE", 20, 5)
    arcpy.AddMessage('\n' + "New Field Added")

    # Create a list of iterable records for our for loop
    ShpRecords = arcpy.UpdateCursor(OutputShapeFile)
    arcpy.AddMessage('\n' + "List made")


    # Generate variable that contains the name of the column containing shape data
    shapefield = arcpy.Describe(OutputShapeFile).shapeFieldName
    arcpy.AddMessage('\n' + "New Field made")


    # Iterate over each index in the shapefile
    for record in ShpRecords:
        # Get the value of the data in the column to be normalzied

        serv_field = "SUM_" + perc_calc[:6]
        tot_field = "SUM_" + total_regions[:6]
        arcpy.AddMessage(tot_field)

        serv_value = record.getValue(serv_field)
        tot_value = record.getValue(tot_field)
        # Normalize the numerator to the area
        result = serv_value/tot_value
        # Save normalized data to the newly calculated value
        record.setValue(OutputField, result)
        ShpRecords.updateRow(record)

    # Get rid of the ShpRecords
    del ShpRecords
    del record


except Exception as e:
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    exceptionreport = sys.exc_info()[2]
    arcpy.AddError("at this location: \n\n" + traceback.format_tb(exceptionreport)[0]+ "\n")
