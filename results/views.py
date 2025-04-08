import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

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
        for sheet_name, df in EXCEL_DATA.items():
            logger.info("Sheet %s loaded with columns: %s", sheet_name, df.columns.tolist())
    except Exception as e:
        logger.exception("Failed to load Excel data: %s", str(e))
        raise

if EXCEL_DATA is None:
    load_excel_data()

def search_excel(request):
    if request.method == 'POST':
        try:
            search_value_raw = request.POST.get('search_value', '').strip()
            if not search_value_raw:
                raise ValueError("Please enter an admission number.")
            search_value = int(search_value_raw)
            logger.info("Searching for admission number: %d", search_value)

            if EXCEL_DATA is None:
                raise FileNotFoundError("Excel data not loaded.")

            for sheet_name, df in EXCEL_DATA.items():
                # Work with a copy to avoid SettingWithCopyWarning
                df = df.copy()

                # Clean DataFrame: Remove "Unnamed" columns
                if not df.empty and df.columns.size > 0:
                    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed", na=False)]
                else:
                    logger.warning("Sheet %s is empty or has no valid columns", sheet_name)
                    continue

                # Normalize column names (remove extra spaces)
                df.columns = df.columns.str.strip()

                # Log columns for debugging
                logger.debug("Sheet %s - Columns after cleaning: %s", sheet_name, df.columns.tolist())

                # Handle rank column renaming
                rank_column = None
                if "درجہ.1" in df.columns:
                    rank_column = "درجہ.1"
                elif "درجہ" in df.columns and df.columns.tolist().count("درجہ") > 1:
                    rank_column = df.columns[df.columns.tolist().index("درجہ", df.columns.tolist().index("درجہ") + 1)]
                if rank_column:
                    df.rename(columns={rank_column: "درجہ (Rank)"}, inplace=True)

                if 'داخلہ نمبر' in df.columns:
                    df['داخلہ نمبر'] = pd.to_numeric(df['داخلہ نمبر'], errors='coerce')
                    result = df[df['داخلہ نمبر'] == search_value]
                    
                    if not result.empty:
                        result_dict = result.iloc[0].to_dict()

                        # Remove unwanted keys
                        result_dict.pop("جائزہ اوسط", None)
                        result_dict.pop("اوسط نمبر", None)
                        result_dict.pop("اوسط نمبر.1", None)

                        # Format numeric values
                        for key, value in result_dict.items():
                            if isinstance(value, (int, float)) and key not in ["داخلہ نمبر", "ہال ٹکٹ نمبر"]:
                                if key == "کل اوسط" and pd.notna(value):
                                    result_dict[key] = "{:.2f}".format(value)
                                elif pd.notna(value):
                                    result_dict[key] = int(value)

                        # Define sections explicitly
                        top_section_keys = ["ہال ٹکٹ نمبر", "داخلہ نمبر", "شعبہ", "درجہ", "نمبر شمار", "نام طالب علم"]
                        bottom_section_keys = ["کل نمبر", "کل اوسط", "درجہ (Rank)", "نتیجہ"]
                        visible_columns = top_section_keys + bottom_section_keys

                        logger.debug("Sheet %s - Visible columns: %s", sheet_name, visible_columns)
                        columns = df.columns.tolist()

                        top_section_data = {key: result_dict.get(key, 'N/A') for key in top_section_keys if key in columns}
                        bottom_section_data = {key: result_dict.get(key, 'N/A') for key in bottom_section_keys if key in columns}
                        middle_section_data = {
                            key: value for key, value in result_dict.items()
                            if key not in visible_columns and key in columns and pd.notna(value)
                        }

                        context = {
                            'top_section_data': top_section_data,
                            'middle_section_data': middle_section_data,
                            'bottom_section_data': bottom_section_data,
                            'class_name': sheet_name,
                            'search_value': search_value
                        }
                        return render(request, 'search_results.html', context)
                else:
                    logger.warning("Sheet %s does not contain 'داخلہ نمبر' column. Available columns: %s", 
                                 sheet_name, df.columns.tolist())

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