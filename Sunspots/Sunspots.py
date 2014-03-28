# CS 101
# Jacob Hayes
#
# Sunspots Smoothing and Graphing
#
# Original Algorithm (Not exactly what this does)
# 1. Open dailysunspots.txt
# 2. Break into lines list
# 3. Average out monthly values:
#     1. Initialize avg dict
#     2. For every year
#         1. For every month
#             1. Initialize count = 0
#             2. Initialize avg = 0
#             3. For every day
#                 1. if sunspots not 999
#                     1. add current element to avg
#                     2. add one to count
#             4. Add avg/count to avg dict with year_month as key
# 4. Write monthly averages out to monthly.txt
# 5. Average the next and previous 6 months to be this month's 'smooth' value
# 6. Write out smooth values to smooth.txt
# 7. Import smooth.txt into Excel and create graph

def data_strip_gen(file_object: 'file_object') -> list:
    '''takes file object
    iterates through file and yields integer year, month, and number of spots'''

    for line in file_object:
        items = line.split()

        year = int(items[0][:4])
        month = int(items[0][4:6])
        spots = int(items[2])

        if int(items[2]) != 999:
            yield [year, month, spots]
# data_strip_gen

def open_file() -> 'file object':
    '''returns an opened file object
    Close file object when done'''

    run_file_open = True

    file = "dailysunspots.txt"
    prompt_file = input("Enter a filename or hit enter for " + file + ": ")
    
    while run_file_open == True:
        if len(prompt_file) != 0:
            file = prompt_file

        try:
            opened_file = open(file)
            run_file_open = False
        except FileNotFoundError:
            print("File was not found\n")
                
            file = "dailysunspots.txt"
            prompt_file = input("Enter a filename or hit enter for " + file + ": ")

    return opened_file

file_ref = open_file()
year_dict = dict()

for year, month, day_spots in data_strip_gen(file_ref):
    if year in year_dict:
        if month in year_dict[year]:
            year_dict[year][month] = [year_dict[year][month][0] + day_spots, year_dict[year][month][1] + 1]
        else:
            year_dict[year].update({month:[day_spots, 1]}) 
    else:
        year_dict[year] = {month:[day_spots, 1]}
file_ref.close()

row_num = 1
monthly_list = []

monthly_file = open('MONTHLY.txt', 'w')
for year in year_dict.keys():
    for month in year_dict[year]:
            year_dict[year][month] = [year_dict[year][month][0]/year_dict[year][month][1], row_num]

            monthly_file.write(str(year) + ' ' + str(month) + ' ' + str(year_dict[year][month][0]) + '\n')
            monthly_list.append([year, month, year_dict[year][month][0], year_dict[year][month][1]])
            row_num += 1
monthly_file.close()

print("Monthly averages created... Written out to MONTHLY.txt")

row_num = 6
smooth_list = []

smooth_file = open('SMOOTH.txt', 'w')
for year, month, spots, row in monthly_list[6:-6]:
    row_num += 1
    months_spots = [spots[2] for spots in monthly_list[row_num - 7:row_num + 6]]
    avg = sum(months_spots)/len(months_spots)

    print(year, month, avg, file = smooth_file)
smooth_file.close()

print("Smoothed averages created... Written out to SMOOTH.txt")
