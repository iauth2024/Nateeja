import pandas as pd

def search_in_excel(file_path, sheet_names, column_name, search_value):
    all_results = pd.DataFrame()
    for sheet_name in sheet_names:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            result = df[df[column_name] == search_value]
            if not result.empty:
                all_results = pd.concat([all_results, result], ignore_index=True)
        except ValueError:
            print(f"Worksheet named '{sheet_name}' not found")
    return all_results

# Prompting user for input
file_path = 'nateeja.xlsx'
search_value = int(input("Enter the search value: "))

sheet_names = [
    'Ifta',
    'Daura Hadees',
    'Mouqoof Alaih (Alif)',
    'Mouqoof Alaih (Baa)',
    'Panjum',
    'Charum',
    'Suwwam Alif',
    'Suwwam Baa',
    'Duwwam  Alif',
    'Duwwam Baa',
    'Duwwam Jeem',
    'Duwwam Madarsa wa School',
    'Awwal Alif',
    'Awwal Aalimiyat Baa',
    'Awwal Aalimiyat jeem',
    'Awwal Madarsa Series',
    'Awwal Schoole series',
    'Idadiyah Madarsa Series ٓ',
    'Idadiyah School Series'
]
column_name = 'داخلہ نمبر'

result = search_in_excel(file_path, sheet_names, column_name, search_value)
print("Rows containing the search value:")
print(result)
