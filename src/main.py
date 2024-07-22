import lib as pyjson


if __name__ == "__main__":
    
    current_file =  '[{"test" : 1}, {"test2" : 2}]'

    json = pyjson.parse_file(current_file)


