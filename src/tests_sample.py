import lib as pyjson


def test_base():
    file = "{}"
    json = pyjson.parse_file(file)

    assert(json == {})

def test_fake_base():
    file = "a{}"
    
    try:
        json = pyjson.parse_file(file)
    except:
        assert(True)


def test_fake_json():
    file = '{a}'
    
    try:
        json = pyjson.parse_file(file)
    except:
        assert(True)

def test_fake_array(): 
    file = '{"test" : ["1"'

    try:
        json = pyjson.parse_file(file)
    except:
        assert(True)

def test_fake_string(): 
    file = '{"test" : "1}'

    try:
        json = pyjson.parse_file(file)
    except:
        assert(True)

def test_fake_key(): 
    file = '{"test : "1"}'

    try:
        json = pyjson.parse_file(file)
    except:
        assert(True)

def test_string():

    file = '{"test" : "String"}'

    json = pyjson.parse_file(file)

    assert(json["test"] == "String")


def test_int():

    file = '{"test" : 100}'

    json = pyjson.parse_file(file)

    assert(json["test"] == 100)


def test_neg():

    file = '{"test" : -100}'

    json = pyjson.parse_file(file)

    assert(json["test"] == -100)


def test_float():

    file = '{"test" : -1.05}'

    json = pyjson.parse_file(file)

    assert(json["test"] == -1.05)


def test_json():
    
    file = '{"test" : {"sub" : 1} }'

    json = pyjson.parse_file(file)

    assert(json["test"]["sub"] == 1)


def test_array_base():
    
    file = '{"test" : [1, "1"] }'

    json = pyjson.parse_file(file)

    assert(json["test"] ==  [1, "1"])


def test_array_nested():

    file = '{"test" : [["1"],{"sub" : 1}]}'

    json = pyjson.parse_file(file)

    array = json["test"]

    assert(array[0][0] == '1')

    assert(array[1]["sub"] == 1)

def test_json_array():

    file = '[{"test" : 1}, {"test2" : 2}]'

    json = pyjson.parse_file(file)

    array = json["root"]

    assert(array[0]["test"] == 1)

    assert(array[1]["test2"] == 2)

    

