import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Cache Excel data at startup
EXCEL_FILE_PATH = os.path.join(settings.BASE_DIR, 'results', 'Nateeja.xlsx')
EXCEL_DATA = None

def load_excel_data():
    global EXCEL_DATA
    try:
        if not os.path.exists(EXCEL_FILE_PATH):
            logger.error("Excel file not found at %s", EXCEL_FILE_PATH)
            raise FileNotFoundError("Excel file not found at the specified path.")
        excel_file = pd.ExcelFile(EXCEL_FILE_PATH)
        EXCEL_DATA = {sheet: pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet) for sheet in excel_file.sheet_names}
        logger.info("Excel data loaded successfully with %d sheets", len(EXCEL_DATA))
    except Exception as e:
        logger.exception("Failed to load Excel data: %s", str(e))
        raise

# Load data on startup (call this in your app’s ready() method or similar)
if EXCEL_DATA is None:
    load_excel_data()

def search_excel(request):
    if request.method == 'POST':
        try:
            # Get search value and convert to integer
            search_value_raw = request.POST.get('search_value', '').strip()
            if not search_value_raw:
                raise ValueError("Please enter an admission number.")
            search_value = int(search_value_raw)
            logger.info("Searching for admission number: %d", search_value)

            if EXCEL_DATA is None:
                raise FileNotFoundError("Excel data not loaded.")

            # Iterate through cached sheets
            for sheet_name, df in EXCEL_DATA.items():
                # Clean DataFrame
                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
                rename_dict = {col: "درجہ (Rank)" for col in df.columns if "درجہ" in col and "1" in col}
                df.rename(columns=rename_dict, inplace=True)

                # Search for student
                if 'داخلہ نمبر' in df.columns:
                    result = df[df['داخلہ نمبر'] == search_value]
                    if not result.empty:
                        result_dict = result.iloc[0].to_dict()

                        # Remove unwanted averages
                        result_dict.pop("جائزہ اوسط", None)
                        result_dict.pop("اوسط نمبر", None)
                        result_dict.pop("اوسط نمبر.1", None)

                        # Format numerical values
                        for key, value in result_dict.items():
                            if isinstance(value, (int, float)) and key not in ["داخلہ نمبر", "رول نمبر"]:
                                if key == "کل اوسط":
                                    result_dict[key] = "{:.2f}".format(value)
                                elif pd.notna(value):
                                    result_dict[key] = int(value)

                        # Handle "درجہ.1" renaming
                        if "درجہ.1" in result_dict:
                            result_dict["درجہ (Rank)"] = result_dict.pop("درجہ.1")

                        # Define sections
                        top_section_keys = ["ہال ٹکٹ نمبر", "داخلہ نمبر", "شعبہ", "درجہ", "نمبر شمار", "نام طالب علم"]
                        bottom_section_keys = ["کل نمبرات", "فیصد", "درجۂ کامیابی", "پوزیشن", "امتیازی پوزیشن", "درجہ (Rank)", "کل اوسط"]
                        visible_columns = top_section_keys + bottom_section_keys

                        columns = df.columns.tolist()
                        top_section_data = {key: result_dict.get(key, 'N/A') for key in top_section_keys if key in columns}
                        bottom_section_data = {key: result_dict.get(key, 'N/A') for key in bottom_section_keys if key in columns}
                        middle_section_data = {key: value for key, value in result_dict.items() 
                                             if key not in visible_columns and key in columns and pd.notna(value)}

                        context = {
                            'top_section_data': top_section_data,
                            'middle_section_data': middle_section_data,
                            'bottom_section_data': bottom_section_data,
                            'class_name': sheet_name,
                            'search_value': search_value
                        }
                        return render(request, 'search_results.html', context)

            message = f"کوئی طالب علم داخلہ نمبر '{search_value}' کے ساتھ کسی شیٹ میں نہیں ملا۔"

        except FileNotFoundError:
            message = "Excel فائل مقررہ راستے پر نہیں ملی۔"
        except ValueError:
            message = "براہ کرم ایک درست داخلہ نمبر درج کریں۔"
        except Exception as e:
            logger.exception("Error processing request: %s", str(e))
            message = f"ایک خرابی پیش آئی: {str(e)}"

        context = {'message': message}
        return render(request, 'search_results.html', context)

    return render(request, 'search_form.html')