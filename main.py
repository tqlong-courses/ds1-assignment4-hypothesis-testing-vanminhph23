import pandas as pd


def normalize(text):
    return text.strip()


def read_university_towns(path_file="university_towns.txt"):
    ct = pd.read_csv(path_file, sep="\t", header=None, names=["all"])

    university_towns = pd.DataFrame(columns=["University", "RegionName", "State"])

    for index, row in ct.iterrows():
        name = row["all"]

        if "[edit]" in name:
            state = normalize(name[0:name.find("[")])
        else:
            index_towns = name.find("(")

            if index_towns <= 0:
                index_towns = name.find(",")

            if index_towns <= 0:
                print(name)
            else:
                towns = normalize(name[:index_towns])
                universities = name[index_towns + 1:]

                str_split = universities.split(",")

                for university in str_split:
                    df = pd.DataFrame({'University': [normalize(university)], 'RegionName': [towns], 'State': [state]})
                    university_towns = university_towns.append(df, ignore_index=True)

    return university_towns


def read_gdp(path_file="gdplev.xls"):
    gdp = pd.read_excel(path_file, skiprows=range(7), header=0)
    gdp.drop(columns=["Unnamed: 0", "Unnamed: 1", "Unnamed: 2", "Unnamed: 3", "Unnamed: 7"], inplace=True)
    gdp.columns = ["year_quarter", "current", "2009"]
    gdp["year"] = gdp.year_quarter.str[0:4].astype(int)
    gdp = gdp[gdp.year >= 2000]

    return gdp


states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def convert_state(state):
    if state in states:
        return states[state]


def read_home(path_file="City_Zhvi_AllHomes.csv"):
    home = pd.read_csv(path_file)

    home["State"] = home["State"].map(lambda x: convert_state(x))

    columns = ["RegionName", "State", "SizeRank"]
    for x in range(2000, 2017):
        for y in range(1, 5):
            if x > 2015 & y > 3:
                break

            column = str(x) + "q" + str(y)

            t1 = str(x) + "-" + str((y - 1) * 3 + 1).zfill(2)
            home[t1] = pd.to_numeric(home[t1], errors='coerce')

            t2 = str(x) + "-" + str((y - 1) * 3 + 2).zfill(2)
            home[t2] = pd.to_numeric(home[t2], errors='coerce')

            if x > 2015 & y > 2:
                home[column] = home[[t1, t2]].mean(axis=1)
            else:
                t3 = str(x) + "-" + str((y - 1) * 3 + 3).zfill(2)
                home[t3] = pd.to_numeric(home[t3], errors='coerce')
                home[column] = home[[t1, t2, t3]].mean(axis=1)

            columns.append(column)

    home = home[columns]

    return home


def get_list_of_university_towns():
    ut = read_university_towns().drop(["University"], axis=1, index=None).drop_duplicates(keep='first').reset_index(drop=True)
    ut.to_csv("University.csv")
    return ut


def get_recession_start():
    gdp = read_gdp()
    for i in range(1, len(gdp) - 1):
        if gdp.iloc[i - 1, 2] > gdp.iloc[i, 2] > gdp.iloc[i + 1, 2]:
            return gdp.iloc[i - 1, 0]

    return None


def get_recession_end():
    gdp = read_gdp()
    is_not_stated = True

    for i in range(1, len(gdp) - 1):
        if is_not_stated:
            if gdp.iloc[i - 1, 2] > gdp.iloc[i, 2] > gdp.iloc[i + 1, 2]:
                is_not_stated = False
        else:
            if gdp.iloc[i - 1, 2] < gdp.iloc[i, 2] < gdp.iloc[i + 1, 2]:
                return gdp.iloc[i + 1, 0]

    return None


def convert_housing_data_to_quarters():
    home = read_home()
    home = home.drop("SizeRank", axis=1)
    home = home.set_index(["RegionName", "State"], drop=True)

    return home


print(get_list_of_university_towns())

print(get_recession_start())

print(get_recession_end())

print(convert_housing_data_to_quarters())
