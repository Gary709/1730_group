"""
Template for the COMP1730/6730 project assignment, S1 2022.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/

Collaborators: u7166705, u7154495, u7326008
"""


def analyse(path_to_file):
    """
    :param path_to_file:
    :return: None
    This is the main function to analyse on provided csv data.
    """

    # Read csv data and save it in `data`
    print("Analysing data file {}".format(path_to_file))
    import csv
    data = []
    with open(path_to_file, 'r') as f:
        for row in csv.reader(f):
            data.append(row)
        f.close()

    # Pre-processing data
    cols = get_col_index(data[0])
    data_unique = unique_country(data[1:], cols)

    # Q1 Start

    # Q1 (a) count the number of unique location
    # find the list of location in the data
    lst_nation = [col[0] for col in data]
    list_nation_result = len(set(lst_nation[1:len(lst_nation)]))
    print("\nQuestion 1:\n")
    print("Number of unique locations: " + str(list_nation_result))
    # Q1 (a) end

    # Q1 (b) count the number of unique country
    # Find the list of unique country in the data
    list_unique_nation = [col[1] for col in data_unique]
    # Delete the same country code and count the length of different country
    list_unique_nation_result = len(set(list_unique_nation[1:len(list_unique_nation)]))
    print("Number of unique countries: " + str(list_unique_nation_result))
    # Q1 (b) end

    # Q1 (c) start
    # find the latest valid vaccine data in every unique country
    country_vaccinated = [col[3] for col in get_specified_data(data_unique, ["total_vaccinations"], cols)]
    # counting
    total_vaccine = count_data(country_vaccinated)
    print("Global vaccine doses: " + str(total_vaccine))
    # Q1 (c) Finished

    # Q1 (d) Start
    # find the latest fst and fully vaccinated people data in unique_country
    country_fst_vaccine = [col[4] for col in get_specified_data(data_unique, ["people_vaccinated"], cols)]
    country_fully_vaccine = [col[5] for col in get_specified_data(data_unique, ["people_fully_vaccinated"], cols)]
    # count the sum of fst and fully vaccinated people
    total_fully_vaccinated = count_data(country_fully_vaccine)
    total_at_least_one_dose = count_data(country_fst_vaccine)
    print("Global population vaccinated: " + str(total_at_least_one_dose))
    print("Global population fully vaccinated: " + str(total_fully_vaccinated))
    # Q1 (d) finished

    # Q2
    print("\nQuestion 2:\n")

    # Q2(a)
    countries = []

    for row in get_specified_data(data_unique, ["people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred",
                                                "people_vaccinated"], cols):
        people_v = int(row[cols['people_vaccinated']])
        people_f_p = float(row[cols['people_fully_vaccinated_per_hundred']])
        people_v_p = float(row[cols['people_vaccinated_per_hundred']])
        # if the population of this country is at least 1 million
        if people_v_p != 0 and people_v / people_v_p * 100 > 1000000:
            countries.append((people_v_p, (row[cols['location']], people_f_p)))
    countries = top_k(countries, 10, True)
    for country in countries:
        print("{}: {}% population vaccinated".format(country[1][0], country[0]))

    # Q2(b)

    for country in countries:
        print("{}: {}% population vaccinated, {:.2f}% partly vaccinated".format(country[1][0], country[0],
                                                                                country[0] - country[1][1]))

    # Q3
    print("\nQuestion 3:\n")

    # Q3(a)

    # earliest_vaccinated_countries = top_k(earliest_vaccinated(data_unique, ['total_vaccinations'], cols), 10)
    earliest_vaccinated_countries = []
    for row in get_specified_data(data_unique, ['total_vaccinations'], cols, True):
        earliest_vaccinated_countries.append((row[cols['date']], row[cols['location']]))
    earliest_vaccinated_countries = top_k(earliest_vaccinated_countries, 10)
    for country in earliest_vaccinated_countries:
        print("{}: first vaccinated on {}".format(country[1], country[0]))

    # Q3(b)

    peek_day_countries = peek_days(data_unique, ['daily_vaccinations'], cols)
    for country in earliest_vaccinated_countries:
        first_date = country[0]
        country_name = country[1]
        peek_date = peek_day_countries[country_name][0]
        peek_num = peek_day_countries[country_name][1]
        print("{}: first vaccinated on {} , {} people vaccinated on {}".format(country_name, first_date, peek_num,
                                                                               peek_date))

    # Q4
    print("\nQuestion 4:\n")

    # Q4(a)

    # Store those countries with a more than 50's fully vaccinated proportion
    valid_f_v_countries = []

    # Just get the latest data with valid column 'people_fully_vaccinated_per_hundred'
    for row in get_specified_data(data_unique, ["people_fully_vaccinated_per_hundred"], cols):

        # Make sure the proportion is higher than 50%
        f_v_proportion = float(row[cols['people_fully_vaccinated_per_hundred']])
        if f_v_proportion > 50:
            valid_f_v_countries.append((f_v_proportion, row[cols['location']]))

    # Pick out the ten with minimal people fully vaccinated proportion
    valid_f_v_countries = top_k(valid_f_v_countries, 10)

    # Q4(b)
    # Prediction equation:
    # population = fully_vaccinated / fully_vaccinated_per_hundred
    # growth_rate = daily_vaccinations(all does) - daily_people_vaccinated(the first does)
    # rest_days = (80% - fully_vaccinated_per_hundred) / growth_rate

    # Sort out the countries with enough information to do prediction
    valid_info_countries = get_specified_data(data_unique,
                                              ['people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
                                               'daily_vaccinations', 'daily_people_vaccinated'], cols)

    # Mapping information with the countries founded in the former step
    for current_proportion, country in valid_f_v_countries:
        for row in valid_info_countries:
            if row[cols['location']] == country:
                detail = row
                break

        # Dealing with situation if one country's info is not enough to predict
        try:

            # Calculating population using fully vaccinated proportion
            population = float(detail[cols['people_fully_vaccinated']]) / \
                         float(detail[cols['people_fully_vaccinated_per_hundred']]) * 100

            # Calculating the rest population to achieve 80% fully vaccinated
            rest_population = population * (80 - current_proportion) / 100

            # Calculating the daily growth by average daily vaccinations subs daily first vaccinated
            daily_growth = float(detail[cols['daily_vaccinations']]) - float(detail[cols['daily_people_vaccinated']])

            # Deal with situation if growth is less or equal than 0
            if daily_growth <= 0: rest_days = "infinite"
            else: rest_days = int(rest_population / daily_growth) + 1

            # Final output of Q(4)
            print("{}: {}% population fully vaccinated, {} days to 80%".format(country, current_proportion, rest_days))
        except TypeError:
            print("{}: {}% population fully vaccinated, but unable to predict how many days to 80%, "
                  "due to lack of information".format(country, current_proportion))


def get_col_index(raw_cols):
    """
    Resolve the column's name and return the index of the column

    :param raw_cols: the plain list of the column, the first row in csv
    :return: the columns -- name indexing dic
    """

    # Searching the column's index with its name
    cols = {}
    for i in range(len(raw_cols)):
        cols[raw_cols[i]] = i
    return cols


def get_specified_data(data, ensure_cols, cols, inverse=False):
    """
    Pick out one latest data for each unique (location, iso_code), by default get latest, or get earliest

    :param data: the raw csv data obtained
    :param ensure_cols: the list of columns that has to be not null
    :param cols: the columns name index
    :param inverse: By default the latest searching, if True, the earliest.
    :return: the data that each unique country with its latest data
    """

    # Use a dictionary to store and update the latest data
    specified_data = []
    specified_dic = {}
    for row in data[1:]:
        # For each unique country, that is (location, iso_code)
        identifier = (row[cols["location"]], row[cols["iso_code"]])

        # If there are some columns that has to be not null, check it
        skip = False
        for ensure_col in ensure_cols:
            if row[cols[ensure_col]] == "":
                skip = True
                break
        if skip:
            continue

        # Find out the row with latest date
        if not inverse:
            if (identifier not in specified_dic) or (specified_dic[identifier][cols["date"]]
                                                     < row[cols["date"]]):
                specified_dic[identifier] = row
        else:
            if (identifier not in specified_dic) or (specified_dic[identifier][cols["date"]]
                                                     > row[cols["date"]]):
                if int(row[cols["total_vaccinations"]]) > 0:
                    specified_dic[identifier] = row

    # Transfer the dictionary to a list and return
    for item in specified_dic.items():
        specified_data.append(item[1])
    return specified_data


def top_k(data, k, reverse=False):
    """
    A sort method to sort the most smallest or largest value from the input data.

    :param data: the data stores (key, value) to be sorted, i.e. (10, "Australia")
    :param k: the most k values
    :param reverse: by default choose the minimum k pairs, otherwise the maximum k pairs
    :return: a list to store the most k (key, value)s
    """

    if len(data) < 2:
        return
    for i in range(len(data)):
        heap_insert(data, i)
    heap_size = len(data)
    data = swap_ele(data, 0, heap_size - 1)
    # size minus one, the last element will not
    # be involved in the further operation
    heap_size -= 1
    while heap_size > 0:
        heapify(data, 0, heap_size)
        data = swap_ele(data, 0, heap_size - 1)
        heap_size -= 1
    # if k is smaller than the length of the dataset
    k = min(k, len(data))
    return list(reversed(data[-k:])) if reverse else data[:k]


def swap_ele(data, pos1, pos2):
    """
    Swap two elements of the given list
    :param data: the data stores (key, value) to be sorted
    :param pos1: position one
    :param pos2: position two
    :return: processed data
    """
    data[pos1], data[pos2] = data[pos2], data[pos1]
    return data


def heapify(data, index, heap_size):
    """
    helper function that is used to build a large root heap
    :param data: the data stores (key, value) to be sorted
    :param index: index of an element
    :param heap_size: the size of the heap
    """
    left = index * 2 + 1
    # if has left child
    while left < heap_size:
        # find the largest child
        largest = left + 1 if left + 1 < heap_size and data[left + 1][0] > data[left][0] else left
        # assign largest to the parent is parent is bigger than largest child
        largest = largest if data[largest][0] > data[index][0] else index
        if largest == index:
            break
        data = swap_ele(data, largest, index)
        index = largest
        left = index * 2 + 1


def heap_insert(data, index):
    """
    helper function that is used to build a large root heap
    :param data: the data stores (key, value) to be sorted
    :param index: index of an element
    """
    while index > 0 and data[index][0] > data[(index - 1) // 2][0]:
        # if the current element is greater than its parent element, swap them
        data = swap_ele(data, index, ((index - 1) // 2))
        index = (index - 1) // 2


def unique_country(data, cols):
    """
    remove regions which have "OWID_" in data
    :param data: the csv data
    :param cols: the columns name index
    :return: list without regions(only have countries)
    """
    # just find the iso_code without OWID_
    unique_country_data1 = [row for row in data if "OWID_" not in row[cols['iso_code']]]

    return unique_country_data1


def peek_days(data, ensure_cols, cols):
    """
    This function return a dictionary that contains country name, and highest vaccinations data
    :param data: the raw csv data obtained
    :param ensure_cols: the list of columns that has to be not null
    :param cols: the columns name index
    :return: a dictionary, format of which is {"country_name": (peek_date, peek_vaccinations_number)}
    """
    peek_dic = {}
    peek_data = {}

    for row in data[1:]:
        # For each unique country, that is (location, iso_code)
        identifier = (row[cols["location"]], row[cols["iso_code"]])

        skip = False
        for ensure_col in ensure_cols:
            if row[cols[ensure_col]] == "":
                skip = True
                break
        if skip:
            continue

        if identifier not in peek_dic or int(peek_dic[identifier][cols['daily_vaccinations']]) < int(
                row[cols['daily_vaccinations']]):
            peek_dic[identifier] = row

    for item in peek_dic.items():
        peek_data[item[1][0]] = (item[1][2], item[1][8])
    return peek_data


def count_data(list_of_col):
    """
    this function return sum of list of string used in Q1
    :param list_of_col: it means the list of the column in the csv
    :return: the sum of the number in the list of string
    """
    total = 0
    for list_number in list_of_col:
        # check is a number or not
        if isinstance(list_number, int) or list_number.isdigit():
            # adding the element to the total
            total += int(list_number)
    return total


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on a CSV file
    analyse('./vaccinations.csv')
    # analyse('./vaccinations_shuffled.csv')
