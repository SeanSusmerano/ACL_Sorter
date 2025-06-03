import math, sys



def _breakup_IPs(content_List_of_List: list) -> list:
    list_of_List_of_IPs = []
    for each_list in content_List_of_List:
        if("deny" in each_list):
            continue

        ip_String = each_list[-1]
        ip_List = ip_String.split('.')

        ip_List[0] = int(ip_List[0])
        ip_List[1] = int(ip_List[1])
        ip_List[2] = int(ip_List[2])
        ip_List[3] = int(ip_List[3])

        list_of_List_of_IPs.append(ip_List)
    return list_of_List_of_IPs


def _bundle_IPs(list_of_Numbers: list) -> list[str]:
    list_of_IPs = []
    while((len(list_of_Numbers)//4) > 0):
        ip_String = f"{list_of_Numbers[0]}.{list_of_Numbers[1]}.{list_of_Numbers[2]}.{list_of_Numbers[3]}"
        list_of_Numbers.pop(3)
        list_of_Numbers.pop(2)
        list_of_Numbers.pop(1)
        list_of_Numbers.pop(0)
        list_of_IPs.append(ip_String)
    
    return list_of_IPs



def _sort_List_of_List(list_of_List, depth = 0):
    if(type(list_of_List[0]) == int):
        return list_of_List
    elif(len(list_of_List) == 1):
        return list_of_List[0]
    elif(len(list_of_List) == 0):
        return []
    
    less_Than_List = []
    equal_List = []
    more_Than_List = []

    median_Index = math.ceil(len(list_of_List)/2)
    try:
        median = list_of_List[median_Index][depth]
    except:
        print(list_of_List)
        print(median_Index)
        print(list_of_List[median_Index])
        print(depth)
        sys.exit()

    equal_List.append(list_of_List[median_Index])
    list_of_List.pop(median_Index)

    for each_List in list_of_List:
        if(depth == 3 and each_List[depth] == median):
            continue
        elif(each_List[depth] == median):
            equal_List.append(each_List)
        elif(each_List[depth] < median):
            less_Than_List.append(each_List)
        elif(each_List[depth] > median):
            more_Than_List.append(each_List)
    
    current_Depth = depth
    new_Depth = depth + 1

    if(less_Than_List == [] and more_Than_List == []):
        return _sort_List_of_List(equal_List, new_Depth)
    elif(less_Than_List != [] and more_Than_List == []):
        return _sort_List_of_List(less_Than_List, current_Depth) + _sort_List_of_List(equal_List, new_Depth)
    elif(less_Than_List == [] and more_Than_List != []):
        return _sort_List_of_List(equal_List, new_Depth) + _sort_List_of_List(more_Than_List, current_Depth)
    else:
        return _sort_List_of_List(less_Than_List, depth = current_Depth) + _sort_List_of_List(equal_List, new_Depth) + _sort_List_of_List(more_Than_List, current_Depth)


def add_Organized_Content(list_Of_Organized_IPs: list, filename = 'organized.txt') -> None:
    file = open(filename, 'a')
    counter = 0

    for each_IP in list_Of_Organized_IPs:
        counter += 1
        ip_Text = f'{counter} permit igmp any host {each_IP}\n'
        file.write(ip_Text)
    
    counter += 1
    ip_Text = f'{counter} deny igmp any any'
    file.write(ip_Text)
    
    file.close()

def clean_Content(content_List: list) -> list[list]:
    new_Content_List = []
    
    for each_Sentence in content_List:
        nested_List = each_Sentence.split(" ")
        nested_List[-1] = nested_List[-1].replace('\n', '')
        if("deny" in nested_List):
            new_Content_List.append(nested_List[-5:])
        elif("permit" in nested_List):
            new_Content_List.append(nested_List[-6:])
        else:
            continue
    
    return new_Content_List

def get_Unorganized_Content(filename = "unorganized.txt") -> list:
    file = open(filename, 'r')
    content = file.readlines()
    file.close()
    return content


def organize_IP(content_List_of_List: list) -> list:
    ip_List = _breakup_IPs(content_List_of_List)
    ip_List_Numbers = _sort_List_of_List(ip_List)
    return _bundle_IPs(ip_List_Numbers)
    

def remove_Unorganized_Content(content_List_of_List: list, filename = 'organized.txt') -> None:
    file = open(filename, 'a')

    for each_List in content_List_of_List:
        list_Text = 'no ' + " ".join(each_List) + '\n'
        file.write(list_Text)
    file.close()


if(__name__ == "__main__"):
    content = get_Unorganized_Content()
    cleaned_Content = clean_Content(content)
    remove_Unorganized_Content(cleaned_Content)
    organized_IP_List = organize_IP(cleaned_Content)
    add_Organized_Content(organized_IP_List)