""" Documentation About This Algorithom """
""" First I count the length of sub string and traverse through the main String with this length of substring and tried to match the sub string with main string in every loop if it is matched I increase the number of count with +1 after finishing the matching function simply return the number of matched we found """




def count_substring(string, sub_string):
    k=len(sub_string)
    l=0
    for i in range(len(string)):

        if string[i:k]== sub_string:
            l=l+1
        k+=1
    return l

count = count_substring(str(input("Enter full string: ")), str(input("Enter sub string: ")))
print(count)