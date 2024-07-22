from collections.abc import Iterator
from typing import Any, Dict, List, Tuple
import sys 

class JSON:
    def __init__(self):
        self.current_json = False
        self.is_json = False
        self.map = {}

class JSONPair:
    def __init__(self):
        self.key = ""
        self.value : Any = None
        self.current_value = False


def get_file() -> str:

    args = sys.argv;

    try:
      file_path = args[1];
      f = open(file_path, "r")
      return f.read()
    except:
        raise Exception("Either incorrect file path or could not open file")


def parse_file(json_file : str) -> Dict:

    json = JSON();

    json_pair = JSONPair();

    json_iter = iter(json_file);

    try:
        while(True):
            parse_json(json_iter,json, json_pair)

    except StopIteration:
        pass

    if(not(json_pair.value == None) and not(json_pair.key == None)):
        json.map[json_pair.key] = json_pair.value

    return json.map


def parse_key(current_json : Iterator[str], json_pair : JSONPair):
    
    current_char : str = next(current_json);

    try:
        while not(current_char == '"'):
            json_pair.key = json_pair.key + current_char;
            current_char = next(current_json);
    except StopIteration:
        raise Exception("Key improperly closed")

    next(current_json)



def parse_string(current_json : Iterator[str]) -> Tuple[str, str]:

    current_char : str = next(current_json);

    current_value = "";

    try:
        while not(current_char == '"'):
            current_value = current_value + current_char;
            current_char = next(current_json);
    except StopIteration:
        raise Exception("String improperly closed")

    current_char = next(current_json)

    return current_value, current_char
        



def parse_number(current_num : str, current_json : Iterator[str], is_negative : bool) -> Tuple[int | float, str]:
    
    current_char : str = current_num;

    current_value : int | float = 0;

    current_digit : int = 0;

    is_float : bool = False;

    try:
        while current_char.isdigit() or current_char == '.':

            if(current_char == '.'):
                is_float = True;
                current_digit = -1;
                current_value = float(current_value);
                current_char = next(current_json);
                continue


            current_num = int(current_char);

            if(current_num == 0 and current_digit > 0 and not(is_float)):
                current_value *= 10;
                current_digit += 1;
                current_char = next(current_json)
                continue


            
            if(is_float):
                if(current_value > 0):
                    current_value += current_num*pow(10,current_digit)
                else:
                    current_value -= current_num*pow(10,current_digit)
            elif(is_negative):
                current_value = current_value*pow(10, current_digit) - current_num;
            else:
               current_value = current_value*pow(10, current_digit) + current_num;
 
            if(is_float):
                current_digit -= 1;
            else:
                current_digit += 1;

            current_char = next(current_json);

    except StopIteration:
        raise Exception("There's an issue with this number")


    return current_value, current_char



def parse_array(json : JSON, current_json : Iterator[str], is_nested : bool) -> List | None:
    
    current_array = [] 
    current_value = None

    if(not(json.current_json)):
        json.current_json = True;


    current_char : str = "";

    try:
        while not(current_char == ']'):
            current_char : str = next(current_json)

            if(current_char.isspace()):
                continue

            if (current_char == '{'):
                sub_json = JSON()
                sub_json.current_json = True
                sub_json_pair = JSONPair()
                
                while(sub_json.current_json):
                    parse_json(current_json, sub_json, sub_json_pair)

                if(not(sub_json_pair.value == None) and not(sub_json_pair.key == None)):
                    sub_json.map[sub_json_pair.key] = sub_json_pair.value

                current_value = sub_json.map

            elif(current_char == '"'):
                current_value, current_char = parse_string(current_json)
            elif(current_char.isdigit() or current_char == '-'):
                if(current_char == '-'):
                    current_char = next(current_json);
                    current_value, current_char = parse_number(current_char, current_json, True);
                else:
                    current_value, current_char = parse_number(current_char, current_json, False);
            elif(current_char == '['):
                current_value = parse_array(json, current_json, True);
            else:
                 if(not(current_char == ',') and not(current_char == ']')):
                    raise Exception("This array is incorrectly delimited")

            if(current_char == ','):
                current_array.append(current_value)
                current_value = None

    except StopIteration:
        raise Exception("There's an issue with this number")

    
    
    if(not(is_nested)):
        json.map["root"] = current_array
    
    if(not(current_value == None)):
        current_array.append(current_value)
    
    return current_array



def parse_json(current_json : Iterator[str], json : JSON, json_pair : JSONPair):

    current_char : str = next(current_json);

    if(current_char.isspace()):
        return

    
    if (current_char == '{'):
        if(json.current_json):
            recursive_pair = JSONPair();
            recursive_json = JSON();
            recursive_json.current_json = True
            
            while(recursive_json.current_json):
                parse_json(current_json, recursive_json, recursive_pair);

            if(not(recursive_pair.value == None) and not(recursive_pair.key == None)):
                recursive_json.map[recursive_pair.key] = recursive_pair.value

            json_pair.value = recursive_json.map
        else:
            json.current_json = True;
    elif(current_char == '"'):
        if(json.current_json):
            if(json_pair.current_value):
                json_pair.value, current_char = parse_string(current_json);
            else:
                parse_key(current_json, json_pair);
    elif(current_char ==':' and json.current_json):
        json_pair.current_value = True
    elif(current_char == ','):
        if(json_pair.key in json.map.keys()):
            raise Exception("Can not have repeat keys")
        else:
            json.map[json_pair.key] = json_pair.value;
    elif(current_char.isdigit() or current_char == '-'):
        if(json_pair.current_value):
            if(current_char == '-'):
                current_char = next(current_json)
                current_number, current_char = parse_number(current_char, current_json, True)
            else:
                current_number, current_char = parse_number(current_char, current_json, False)

            json_pair.value = current_number
    elif(current_char == '['):
         if(json.current_json):
            json_pair.value = parse_array(json, current_json, True);
         else:
            parse_array(json, current_json, False)
    else:
        if(not(current_char == '}')):
            raise Exception("Need to start a JSON object before any non-whitespaces")

    if(current_char == '}'):
        if(json.current_json):
            json.current_json = False;
            json.is_json = True;
        else:
            raise Exception("A JSON Object was never started")

        
         

                

            
        



