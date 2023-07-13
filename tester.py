def parse_bl_string(bl_string: str) -> dict:
    """
    Parses a string representing a drawing template and returns a dictionary

    The input string should have the following format:
    "street_name,landbase,choice,house1,house2,measurement"

    The function returns a dictionary with the following keys:
    - street_name: a string representing the name of the street
    - landbase: a string representing the direction of the landbase (n, e, s, w)
    - choice: a string representing the choice (o, i, se, nw)
    - house1: a string representing the first house number
    - house2: a string representing the second house number
    - measurement: a string representing the measurement (a positive integer)

    If the input string does not have the expected format, the function returns None.
    """
def parse_bl_string(bl_string):
    
    bl_list = bl_string.split(",")
    if len(bl_list) != 6:
        return None
    else:
        # check that landbase is one of n,e,s,w
        if bl_list[1].strip() not in ["n", "e", "s", "w"]:
            return None
        # check that choice is one of o,i,se,nw
        if bl_list[2].strip() not in ["o", "i", "se", "nw"]:
            return None
        # check that measurement is a positive integer
        if not bl_list[5].strip().isdigit():
            return None 
        bl_dict = {
            "street_name": bl_list[0].strip().upper(),
            "landbase": bl_list[1].strip(),
            "choice": bl_list[2].strip(),
            "house1": bl_list[3].strip(),
            "house2": bl_list[4].strip(),
            "measurement": bl_list[5].strip(),
        }
        return bl_dict
    
print(parse_bl_string("connie cres, n, o, 2, 4, 10"))
