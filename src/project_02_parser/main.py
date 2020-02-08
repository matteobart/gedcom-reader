import argparse
import family
import person 

people = {}
families = {}

#given an array of strings parse the GEDCOM information
#there is no return but will print to console
def parse(lines):
    for line in lines:
        line = line.replace("\n", "")
        print_in(line)
        split = line.split(" ", 2)
        if len(split) == 2: #if it has no extra args, add an empty one
            split.append("")

        if split[0] == "0":
            if split[2] == "INDI":
                print_out(0, "INDI", True, split[1])
            elif split[2] == "FAM":
                print_out(0, "FAM", True, split[1])
            elif split[1] == "HEAD":
                print_out(0, "HEAD", True, split[2])
            elif split[1] == "TRLR":
                print_out(0, "TRLR", True, split[2])
            elif split[1] == "NOTE":
                print_out(0, "NOTE", True, split[2])
            else:
                print_out(0, split[1], False, split[2])
        elif split[0] == "1":
            possible_tags = [
                "NAME", 
                "SEX", 
                "BIRT", 
                "DEAT", 
                "FAMC", 
                "FAMS", 
                "MARR", 
                "HUSB", 
                "WIFE",
                "CHIL",
                "DIV"
                ]
            if split[1] in possible_tags:
                print_out(1, split[1], True, split[2])
            else:
                print_out(1, split[1], False, split[2])
        elif split[0] == "2":
            if split[1] == "DATE":
                print_out(2, "DATE", True, split[2])
            else:
                print_out(2, split[1], False, split[2])
        else: 
            print_out(split[0], split[1], False, split[2])
def print_in(str):
    print("-->", str)

def print_out(level, tag, valid, arg):
    print("<--", str(level) + "|" + str(tag) + "|" + ("Y" if valid else "N") + "|" + str(arg))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Homemade GEDCOM reader')
    parser.add_argument('GEDCOM_file', type=str, help='The file to read (must be in GEDCOM format')
    args = parser.parse_args()
    
    with open(args.GEDCOM_file) as file:
        lines = file.readlines()
        parse(lines)


