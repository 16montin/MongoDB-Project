import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
import pprint
import codecs
import json

def count_tags(filename):
        tags ={}
        for moment, part in ET.iterparse(filename):
            if part.tag not in tags.keys():
                tags[part.tag] = 1
            else:
                tags[part.tag] += 1
        return tags
        


def test1():
        filename = 'C:\\Users\\Nicole\\Desktop\\pittsburgh.osm'
        tags = count_tags(filename)
        pprint.pprint(tags)

    

if __name__ == "__main__":
    test1()



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == 'tag':
        k = element.attrib['k']
        if re.search(lower,k):
            keys['lower'] +=1
        elif re.search(lower_colon,k):
            keys['lower_colon'] +=1
        elif re.search(problemchars,k):
            keys['problemchars'] +=1
        else:
            keys['other'] += 1
            
    return keys
    



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test2():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('C:\\Users\\Nicole\\Desktop\\pittsburgh.osm')
    pprint.pprint(keys)
    


if __name__ == "__main__":
    test2()


def get_user(element):
    if 'uid' in element.attrib.keys():
       return element.attrib['uid']
    else:
        return False
    


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        user = get_user(element)
        if user != False:
            users.add(user)
    return users



def test3():

    users = process_map('C:\\Users\\Nicole\\Desktop\\pittsburgh.osm')
    pprint.pprint(users)
    print(len(users))



if __name__ == "__main__":
    test3()



street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Center", "Alley", "Circle",
            "Connector", "Cove", "Crossing", "End", "Expressway","Extension", "Harbor",
            "Heights", "Highway", "Hill", "Park", "North", "South", "East", "West"
            "Pike", "Plaza", "Run", "Entrance", "Allegheny", "Terrace", "Way", "Bridge"]
problemvals = ['19', '837', "Allies", "Dowling", "Eisele", "Harding",
               "Weir", "Joanne", "Lysle", "Maples", "McAleer", "Marshall", "Maurers",
               "Oaks", "Patricia", "Penco", "Strasse", "Trillium", "Walnut"
               "Wheel-in-Campround", "18", "202", '228', "30", "51", "519",
               "8", "885", "910", "941"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "S": "Street",
            "ST": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Ave": "Avenue",
            "Av.": "Avenue",
            "Av": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.":"Boulevard",
            "Brdg": "Bridge",
            "CT": "Court",
            "Ct": "Court",
            "DR": "Drive",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Hwy": "Highway",
            "Ln": "Lane",
            "Pl": "Plaza",
            "Sq": "Square",
            "Ter": "Terrace",
            "W": "Way",
            "center": "Center"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in problemvals:
            return None
        elif street_type not in expected:
            street_types[street_type].add(street_name)
        


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = codecs.open(osmfile, "r", encoding='utf-8')
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    
               
    return street_types


def update_name(name, mapping):
    name_list = name.split(' ')
    street_abbreviation = name_list[-1]
    new_name = ' '.join(name_list[:-1])
    name = new_name + ' ' + mapping[street_abbreviation]
    
    return name

def test4():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_name(name, mapping)
            print (name), "=>", better_name
            


if __name__ == '__main__':
    test4()





CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node['created'] = {}
    node['pos'] = {}
    address = {}
                
    if element.tag == "node" or element.tag == "way" :
        node["id"] = element.attrib["id"]
        node["type"] =  element.tag
        node[ "visible"] = element.get("visible")
        created = {}
        created["version"] = element.attrib["version"]
        created["changeset"] = element.attrib["changeset"]
        created["timestamp"] = element.attrib["timestamp"]
        created["user"] = element.attrib["user"]
        created["uid"] = element.attrib["uid"]
        node["created"] = created
        if "lat" in element.keys() and "lon" in element.keys():
           pos = [element.attrib["lat"], element.attrib["lon"]]        
           node["pos"] = [float(string) for string in pos]
        else:
           node["pos"] = None

        for tag in element.iter("nd"):
            if not node.has_key("node_refs"):
                node["node_refs"] = []
            node["node_refs"].append(tag.attrib['ref'])
            
        for tag in element.iter("tag"):
            key = tag.attrib["k"]
            value = tag.attrib["v"]
            
            if "addr" in key:
               if "addr:street" in key:
                    if "name" not in key and "prefix" not in key and "type" not in key:
                        address['street'] = value
               else:
                 add_key = key.split(":")[1]
                 address[add_key] = value
            elif len(key) < 3:
                new_key = key.split(":")[1]
                address[new_key] = value
            elif address:
                node["address"] = address
        return node

    else:
        return None

   
    
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)

            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test5():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('C:\\Users\\Nicole\\Desktop\\pittsburgh.osm', False)
    
    print (data)


if __name__ == "__main__":
    test5()
