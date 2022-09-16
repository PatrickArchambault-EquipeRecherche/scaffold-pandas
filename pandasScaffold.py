#!/usr/bin/python

"""A set of functions to make working with Python Pandas a little easier,
and to collect idioms and patterns that are useful."""

import pandas

###### Functions ######

# Collect the elements of a series by type - may be used for counting, but
# also has utility for testing for maximum and minimum values in 
# mixed-composition series

def byType( series , printout=False ):
    integers = []
    strings = []
    floats = []
    booleans = []
    nones = []
    others = []

    for element in series:
        if type(element) == int:
            integers.append(element)
        elif type(element) == str:
            strings.append(element)
        elif type(element) == float:
            floats.append(element)
        elif type(element) == bool:
            booleans.append(element)
        elif type(element) == None:
            nones.append(element)
        else:
            others.append(element)
    
    output = {
                "integers":integers,\
                "strings":strings,\
                "floats":floats,\
                "booleans":booleans,\
                "nones":nones,\
                "others":others\
            }

    if printout == True:
        po = f"Integers: {len(output['integers'])}\n"
        po = po + f"Strings: {len(output['strings'])}\n"
        po = po + f"Floats: {len(output['floats'])}\n"
        po = po + f"Booleans: {len(output['booleans'])}\n"
        po = po + f"Nones: {len(output['nones'])}\n"
        po = po + f"Others: {len(output['others'])}\n"

        print(po)
    
    return output


# Take a column, run byType on it, and return the proportions of each type. 
# Mostly an intermediate step to looking for outliers, 
# minimum and maximum values, dates, etc.

def proportionOfTypes( columnname , printout=False ):
    mytypes = byType(columnname)
    total_length = len(columnname)
    int_prop = len(mytypes["integers"]) / total_length * 100
    str_prop = len(mytypes["strings"]) / total_length * 100
    float_prop = len(mytypes["floats"]) / total_length * 100
    boolean_prop = len(mytypes["booleans"]) / total_length * 100
    none_prop = len(mytypes["nones"]) / total_length * 100
    other_prop = len(mytypes["others"]) / total_length * 100

    output = {
                "integers"  :   int_prop,\
                "strings"   :   str_prop,\
                "floats"    :   float_prop,\
                "booleans"  :   boolean_prop,\
                "nones"     :   none_prop,\
                "others"    :   other_prop\
            }

    if printout == True:
        po = f"Integers: {int_prop}\n"
        po = po + f"Strings: {str_prop}\n"
        po = po + f"Floats: {float_prop}\n"
        po = po + f"Booleans: {boolean_prop}\n"
        po = po + f"Nones: {none_prop}\n"
        po = po + f"Others: {other_prop}\n"

        print(po)

    return output


# Convert all elements of a list to some Type - useful for harmonizing list of 
# numbers for getting maximum and minimum values.

def typeCoerce( mylist , dtype=float ):
    return list(map(dtype, mylist))


# Return a dictionary with the maximum and minimum values of one or more lists.
# If not all of the values are the same type (intgers, floats) then we convert 
# all of the elements to floats and then return the maximum and minimum values.

def minMaxNumbers( *lists ):
    if len(lists) > 1:
        #print("Several lists.")
        list_element_types = []
        all_list_elements = []
        for lst in lists:
            for item in lst:
                list_element_types.append(type(item))
                all_list_elements.append(item)
        if len(set(list_element_types)) == 1:
            minimum = pandas.Series(all_list_elements).min()
            maximum = pandas.Series(all_list_elements).max()
        else:
            #print(all_list_elements)
            coerced_list = typeCoerce(all_list_elements)
            minimum = pandas.Series(coerced_list).min()
            maximum = pandas.Series(coerced_list).max()
        #print(lists)
    else:
        #print("Just one list.")
        minimum = pandas.Series(lists[0]).min()
        maximum = pandas.Series(lists[0]).max()
        
    return {"minimum":minimum, "maximum":maximum}


# Find outliers in a column, characterize the data, count outliers, nulls

def inspect_column( columnname ):
    desc = f"""{columnname}\n
    Nulls: {columnname.isna().sum()}"""


    return desc


# Index on datetime column

def makeDateTimeIndex( dataframe , columnname ):
    """
    Usage example:
    hr = makeDateTimeIndex( pandas.read_csv("myCSVfile.csv"), "nameOfDateTimeColumnToIndexOn" )
    """
    dataframe[columnname] = pandas.to_datetime( dataframe[columnname] )
    dataframe = dataframe.set_index( dataframe[columnname] )

    return dataframe


# Plot rows over time, based on a rows-per-interval approach

def plotRowsOverTime( dataframe , frequency ):
    """
    The dataframe has to be using a datetime column as the index.
    You then specify the frequency that you are looking for results on, i.e.
    day, month, year, etc.
    Day = D
    Month = M
    Read "pandas Grouper" documentation for details.
    """
    dataframe.groupby(pandas.Grouper(freq=frequency)).size().plot()


###### Patterns ######

# Connect two or more dataframes together that probably overlap, dropping 
# whatever is duplicated
firstDataFrame = pandas.DataFrame()
secondDataFrame = pandas.DataFrame()
newDataFrame = pandas.concat( [firstDataFrame , firstDataFrame] ).drop_duplicates()


# Change the encoding of NotANumber on import - useful when your data has 
# inadvertent entries that are not null, like sodium (NA)
from pandas._libs.parsers import STR_NA_VALUES

disable_na_values = { "NA" }
my_default_na_values = STR_NA_VALUES - disable_na_values
df = pandas.read_csv( "myCSVfile.csv" , na_values = my_default_na_values )


# Pad out values with 4 leading zeros on pandas.read_csv()
df = pandas.read_csv("myCSVfile.csv", converters={'UnpaddedColumn1': '{:0>4}'.format, 'UnpaddedColumn2': '{:0>4}'.format}) 


# Filter a dataframe into a subset that all meets a criteria.
# In the example case, we use pandas.factorize() to get all of the values, 
# because it _should_ be a small set, but there are mispellings, other 
# weirdness that we have to find, so this pattern lets us group all rows 
# that have the set of values in the list

pos = ['DÉTECTÉ', 'DÉTEDÉTECTÉ', 'detecté', 'detecte', '03DÉTECTÉ']

posCases = firstDataFrame[firstDataFrame["RESULTAT"].isin(pos)]

