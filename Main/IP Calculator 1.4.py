class Bcolors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    FAIL = '\033[7;91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def cal_address(iln):
    if iln[3] == 255:
        iln[3] = 0
        iln[2] += 1
        da = list_to_str(iln)
    else:
        int_list_netip[3] += 1
        da = list_to_str(iln)
    return da


def write_in_file(pr, file_name):
    with open(file_name, 'a+') as file:
        file.writelines('')
        file.write(pr)
        file.close()


def and_gen_ip(old_ip, bin_mask):
    new_ip = ""
    for i in range(35):
        if old_ip[i] == "1" and bin_mask[i] == "1":
            if old_ip[i] == ".":
                new_ip += "."
            else:
                new_ip += "1"
        else:
            if old_ip[i] == ".":
                new_ip += "."
            else:
                new_ip += "0"
    return new_ip


def bin_to_dec(bin_ip):
    listed_ip = bin_ip.split(".")
    new_ip = ""
    for i in range(4):
        bin_oct = listed_ip[i]
        oct = 0
        for j in range(8):
            k = bin_oct[j]
            if k == "1":
                oct += 2 ** (8 - j - 1)
            elif k == "0":
                oct += 0
        new_ip += str(oct)
        if i != 3:
            new_ip += "."
    return new_ip


def cal_bin_mask(mask_num):
    listed_mask = []
    mask_len = 32
    for i in range(mask_num):
        listed_mask += "1"

    for i in range(mask_len - mask_num):
        listed_mask += "0"

    bin_mask = ""
    for i in range(mask_len):
        if i == 8 or i == 16 or i == 24:
            bin_mask += "."
        bin_mask += listed_mask[i]

    return bin_mask


def bin_ip_transform(f):
    transformed = '.'.join([bin(int(x) + 256)[3:] for x in f.split('.')])
    return transformed


def list_to_str(l):
    string = ""
    for i in range(4):
        letter = str(l[i])
        string += letter
        if i != 3:
            string += "."
    return string


# Errors
def error_01():
    print(Bcolors.FAIL + "Error 01: Invalid IP")
    print(Bcolors.END + "")


def error_02():
    print(Bcolors.FAIL + "Error 02: Invalid Mask")
    print(Bcolors.END + "")


def error_03():
    print(Bcolors.FAIL + "Error 03: Please use only numbers")
    print(Bcolors.END + "")


true_one = True
true_two = True

# Getting IP from a user
while true_one:
    ip = input("Please enter IP: ")
    split_ip = ip.split(".")
    split_ip_len = len(split_ip)

    if split_ip_len == 4:
        try:
            int_split_ip = [int(i) for i in split_ip]
            nothing = 0
            for a in int_split_ip:
                if a < 0 or a > 255:
                    error_01()
                    break
                else:
                    nothing += 1
            if nothing == 4:
                true_one = False
        except ValueError:
            error_01()
    else:
        error_01()

# Changing IP to binary
binary_ip = bin_ip_transform(ip)

# Getting mask from a user
while true_two:
    try:
        mask = int(input("Please enter the mask: "))
        # Checking if mask is valid
        if 32 < mask or 0 > mask:
            error_02()
        else:
            break
    except ValueError:
        error_02()

# Calculating binary mask
binary_mask = cal_bin_mask(mask)

# Getting number of network from user
while true_two:
    try:
        subnets_number = int(input("Please enter number of network: "))
        break
    except ValueError:
        error_03()

# Getting number of host from a user
while True:
    try:
        hosts_number = int(input("Please enter number of host: "))
        break
    except ValueError:
        error_03()

# Calculating general network IP
binary_net_ip = and_gen_ip(binary_ip, binary_mask)
dec_net_ip = bin_to_dec(binary_net_ip)

# Calculating new mask and converting it to binary
n = 0
while True:
    n += 1
    if 2 ** n >= subnets_number:
        new_mask = mask + n
        break

binary_new_mask = cal_bin_mask(new_mask)

# Getting new hosts number
m = 0
while True:
    m += 1
    if 2 ** m >= hosts_number + 2:
        new_hosts_number = 2 ** m - 2
        break

# Creating new file
with open('Num', 'r') as fl:
    a = fl.read()
    fl.close()

with open('Num', 'w') as fl:
    b = int(a) + 1
    fl.write(str(b))

new_file_name = 'Address_'
new_file_name += str(b)

# Writing in the file, network IP in dec system and bin system
with open(new_file_name, 'a') as nfl:
    nfl.write("The network IP is " + dec_net_ip + " | Binary system: " + binary_net_ip + '\n')
    nfl.close()

# Splitting IP to the list
split_netip = dec_net_ip.split(".")
int_list_netip = [int(x) for x in split_netip]


dec_address = dec_net_ip
str_bin_address = ""
subnet_address_num = 1

# Calculating dots number in mask
mask_dot_num = 0
if new_mask > 8:
    mask_dot_num = 1
elif new_mask > 16:
    mask_dot_num = 2
elif new_mask > 24:
    mask_dot_num = 3

# Loading
loading = 100 / subnets_number
ready_loading = 0

# Main loop
for w in range(subnets_number):
    # Calculating subnets addresses
    if w == 0:
        # Calculating first subnet address
        p = "The " + str(subnet_address_num) + " subnet address is " + dec_address + '\n'
        write_in_file(p, new_file_name)
    else:
        # Calculating subnets addresses
        cal_address(int_list_netip)
        p = "The " + str(subnet_address_num) + " subnet address is " + dec_address + '\n'
        write_in_file(p, new_file_name)

    # Loop for calculating hosts addresses
    for c in range(new_hosts_number):
        cal_address(int_list_netip)
        p = "The address of host " + str(c + 1) + " is " + dec_address +\
            " in " + str(subnet_address_num) + " subnet" + '\n'
        write_in_file(p, new_file_name)

    # Calculating broadcast address
    cal_address(int_list_netip)
    p = "The broadcast address in " + str(subnet_address_num) + " subnet is " + dec_address + '\n'
    write_in_file(p, new_file_name)

    subnet_address_num += 1

    # Loading message
    ready_loading += loading
    print(Bcolors.CYAN + "Loading " + str(round(ready_loading)) + "%" + Bcolors.END)

# Finish message
print(Bcolors.GREEN + "Done")
print("Thank you for using my IP calculator")
