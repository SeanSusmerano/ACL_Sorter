import sort_ACL

def get_IP_List(list_of_Sentences: list):
    list_of_IPs = []

    for each_sentence in list_of_Sentences:
        list_of_IPs.append(each_sentence[-1])
    
    return list_of_IPs


def main():
    IPs_Text_List= sort_ACL.get_Unorganized_Content("check_IPs.txt")

    counter = 0
    for each_IP in IPs_Text_List:
        IPs_Text_List[counter] = each_IP.strip('\n')
        counter += 1

    print(IPs_Text_List)

    IPs_Text_Block = sort_ACL.get_Unorganized_Content()
    IPs_Sentence_List = sort_ACL.clean_Content(IPs_Text_Block)

    list_of_IPs = get_IP_List(IPs_Sentence_List)

    file = open("check_IPs.txt", "w")

    for each_IP in IPs_Text_List:
        if(each_IP in list_of_IPs):
            ip_Index = list_of_IPs.index(each_IP)

            sentence_to_Write = " ".join(IPs_Sentence_List[ip_Index])
            file.write(sentence_to_Write + "\n")
        else:
            file.write(f"{each_IP}: Could not be found.\n")
    
    file.close()


if(__name__ == "__main__"):
    main()