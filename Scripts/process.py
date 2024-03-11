from bs4 import BeautifulSoup
import requests
import openpyxl
import csv
import os


def get_html_content(url):
    response = requests.get(url)
    return response.content


def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table_div = soup.find('div', class_='table-block mb-1')
    table = table_div.find('table', class_='publication-table')
    table_rows = table.find_all('tr')

    data = []
    for row in table_rows:
        cells = row.find_all(['td', 'th'])
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    return data


def rename_columns(data, new_column_names):
    if len(data) > 0:
        for i in range(len(data[0])):
            if i < len(new_column_names):
                data[0][i] = new_column_names[i]


def replace_null_x_dash(data):
    for row in data:
        for i in range(len(row)):
            if row[i].lower() in {"null", "x", "-"}:
                row[i] = "0"


def remove_empty_rows(data):
    data[:] = [row for row in data if any(cell.strip() != "0" for cell in row)]


def save_to_excel(data, file_path):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    for row_data in data:
        worksheet.append(row_data)

    workbook.save(file_path)


def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


def clean_data(data):
    # Replace "null", "x", "-" values with "0"
    replace_null_x_dash(data)
    # Remove rows containing only "0"
    remove_empty_rows(data)


def main():
    url = "https://stat.gov.kz/ru/industries/social-statistics/stat-culture/publications/6115/"

    html_content = get_html_content(url)
    table_data = extract_table_data(html_content)

    # Rename columns
    new_column_names = ["Regions", "Theaters", "Museums", "Cultural and leisure facilities",
                        "Cinemas", "Libraries", "Concert organizations", "Parks", "Zoos", "Circuses"]
    rename_columns(table_data, new_column_names)

    # Save data to Excel and CSV files
    excel_file_path = "archive/1.xlsx"
    csv_file_path = "data/1.csv"
    save_to_excel(table_data, excel_file_path)
    save_to_csv(table_data, csv_file_path)

    # Clean data by replacing "null", "x", "-" values with "0" and removing empty rows
    clean_data(table_data)

    # Save cleaned data to new files
    cleaned_excel_file_path = "archive/information.xlsx"
    cleaned_csv_file_path = "data/output.csv"
    save_to_excel(table_data, cleaned_excel_file_path)
    save_to_csv(table_data, cleaned_csv_file_path)

    print(f"Data extracted, cleaned, and saved to:\n- {cleaned_excel_file_path}\n- {cleaned_csv_file_path}")


if __name__ == "__main__":
    main()


def delete_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error deleting file '{file_path}': {e}")


files_to_delete = ['data/1.csv', 'archive/1.xlsx']
delete_files(files_to_delete)