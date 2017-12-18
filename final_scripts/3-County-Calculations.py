'''
---------------------------------------------------------------------------------------------------------
| Part 3 of 3 of the census-based service area calculator.                                              |
| To use this toolkit, you will need a network layer of roads, a feature class of facility locations,   |
| census block level demographic data, and a shapefile of the counties encompassing the facilities.     |
|                                                                                                       |
| This script takes the following inputs:                                                               |
|                                                                                                       |
| input_part_2  = output of Part 1, a shapefile containing areas of service area by census block        |
| input_census_file  = county-level shapefile                                                           |
| 																										|
| percent_coverage = field within input_part_2 containing percent coverage of service area              |
| census_input_field = user-specified field within input_part_2 containing demographic data             |
| dissolve_field = FID or unique object identifier within incput_census_file to dissolve on             |
| 																										|
| total_serve_output = output field containing total number of served peoples of chosen demographic     |
| percent_serve_output = output field containing the percentage of people in demographic in county 		|
|                        that are served by the facilities  											|
|                                                                                                       |
| output_shapefile = location of output shapefile                                                       |
|                                                                                                       |
---------------------------------------------------------------------------------------------------------

'''



import sys, math, string, arcpy, os, traceback

arcpy.env.overwriteOutput = True

try:


    # Set input files
    input_part_2         = arcpy.GetParameterAsText(0) # input shapefile
    input_census_file    = arcpy.GetParameterAsText(1) # input census file
    arcpy.AddMessage('\n' + "The input shapefiles are" + input_part_2 + input_census_file)

    # Set input variables
    percent_coverage     = arcpy.GetParameterAsText(2) # percent coverage field from input_part_2
    census_input_field   = arcpy.GetParameterAsText(3) # census input data
    dissolve_field       = arcpy.GetParameterAsText(4) # county FID

    # Set output variables
    total_serve_output   = arcpy.GetParameterAsText(5) # output - service area % * census value
    percent_serve_output = arcpy.GetParameterAsText(6) # output - total_serve_outpute / census_input_field
    arcpy.AddMessage("The name of the fields to be added are " + total_serve_output + " and " + percent_serve_output + "\n")

    # Set output file
    OutputShapeFile      = arcpy.GetParameterAsText(7)
    arcpy.AddMessage('\n' + "The output shapefile is" + OutputShapeFile)


    # Add field to the input shapefile that will store the total serviced population of 
    # input census variable
    arcpy.AddField_management(input_part_2, total_serve_output, "DOUBLE", 20, 5)

    # Create a list of iterable records to loop through
    ShpRecords_calc_number = arcpy.UpdateCursor(input_part_2)

    # Iterate over each index in the shapefile
    for record in ShpRecords_calc_number:
        census_value = record.getValue(census_input_field)         # get value of user-specified census field
        percent_coverage_value = record.getValue(percent_coverage) # get value of percent coverage for census tract
        result = census_value * percent_coverage_value             # calculate total number of serviced population for census tract
        record.setValue(total_serve_output, result)                # save that result
        ShpRecords_calc_number.updateRow(record)

    del ShpRecords_calc_number
    del record

    # Intersection between input data and input census file, in order to attach county-level unique object identifier
    outPutIntersect = arcpy.Intersect_analysis([input_part_2, input_census_file],
                             join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="INPUT")

    # Dissolve the layer on the county boundaries, summing up the served and total populations for each census tract
    dissolved = arcpy.Dissolve_management(in_features=outPutIntersect,
                              out_feature_class=OutputShapeFile,
                              dissolve_field=dissolve_field, statistics_fields=census_input_field + " SUM;" + total_serve_output + " SUM",
                              multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")


    # Add a field to contain the percentage of county-wide population served by the facilities
    arcpy.AddField_management(OutputShapeFile, percent_serve_output, "DOUBLE", 20, 5)
    arcpy.AddMessage('\n' + "New Field Added")

    # Create a list of iterable records to loop through
    ShpRecords = arcpy.UpdateCursor(OutputShapeFile)
    arcpy.AddMessage('\n' + "List made")


    # Generate variable that contains the name of the column containing shape data
    shapefield = arcpy.Describe(OutputShapeFile).shapeFieldName
    arcpy.AddMessage('\n' + "New Field made")


    # Iterate over each index in the shapefile
    for record in ShpRecords:
        serviced = "SUM_" + total_serve_output[:6] # generate field name column for the serviced population computed when dissolving
        total = "SUM_" + census_input_field[:6]    # generate field name column for the total population computed when dissolving
        arcpy.AddMessage(serviced)                 # print to console in order to confirm that the operation worked

        serv_value = record.getValue(serviced)     # get the value of the serviced population
        tot_value = record.getValue(total)         # get the value of the total population
        result = serv_value/tot_value              # calculate the percent of population served
        
        record.setValue(percent_serve_output, result)
        ShpRecords.updateRow(record)

    # Get rid of the ShpRecords
    del ShpRecords
    del record


except Exception as e:
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    exceptionreport = sys.exc_info()[2]
    arcpy.AddError("at this location: \n\n" + traceback.format_tb(exceptionreport)[0]+ "\n")
