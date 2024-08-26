
data = ['82', '0a', '10', '08', '04', '02', '01', '02', '02', '02', '02', '09', '00', '82', '0b', '10', '04', '03', '02', '01', '08', '04', '82', '0c', '10', '0c', '06', '03', '06', '03', '06', '03', '06', '03', '06', '03', '02', '09', '02']

def command(cod):
    if (cod == "0a"):
        return "Gerilim"
    elif (cod == "0b"):
        return "Akım"
    elif (cod == "0c"):
        return "Sıcaklık"
    else: return "Wrong Code"

def typeOfMessage(messageType):
    if (messageType == "10"):
        return "Hex"
    elif (messageType == "20"):
        return "Decimal"
    elif (messageType == "30"):
        return "Binary"
    else: return "Wrong Code"

def lenghtOfData(data):
    myList = []
    for i in data[3:-2]:
        myList.append(i)

    return len(myList)

def sum_hex_values_and_modulo(hex_list):
    # Convert each hexadecimal string to an integer and sum them up
    total_sum = sum(int(x, 16) for x in hex_list[:-1])
    # Calculate the modulo by 9
    result = total_sum % 9
    return result







def sepFunc(data):
    indices = [index for index, value in enumerate(data) if int(value, 16) > 0x80]
    return indices

def slice_hex_list(data, indexes):
    sliced_parts = []
    for i in range(len(indexes)):
        start = indexes[i]
        if i + 1 < len(indexes):
            end = indexes[i + 1]
        else:
            end = len(data)
        sliced_parts.append(data[start:end])
    return sliced_parts

def interpretation(data):
    print("Data is here")
    print(data)
    if str(data[0]) > "80":
        #print(f" Header is:{data[0]}")
        for i in range(len(data)):
            print(data[i])
            komut=command(data[i][1])
            tip=typeOfMessage(data[i][2])
            uzunluk=lenghtOfData(data[i])
            CRC = sum_hex_values_and_modulo(data[i])
            print(f"Header  :{data[i][0]}\n"
                  f"Komut   :{komut}\n"
                  f"Tip     :{tip}\n"
                  f"Uzunluk :{uzunluk}\n"
                  f"Değerler:{data[i][4:4+uzunluk]}\n"
                  f"CRC     :{CRC}\n")




# print(slice_hex_list(data,sepFunc(data)))
# print(slice_hex_list(data,sepFunc(data))[2])

#interpretation(slice_hex_list(data,sepFunc(data)))
#print(sepFunc(data))


# print("asdadasdaddaasddsadsaasd")
# print(slice_hex_list(data,sepFunc(data)))
#
# print("asdadasdda")
# print(hex_sum(data))
interpretation(slice_hex_list(data,sepFunc(data)))
