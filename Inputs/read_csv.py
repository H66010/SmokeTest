import csv

def read_csv_data(file_path, encoding='utf-8'):
    usernames = []
    passwords = []

    try:
        with open(file_path, newline='', encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # 行の長さを確認し、適切なデータのみ追加
                if len(row) >= 2 and row[0] and row[1]:
                    usernames.append(row[0].strip())
                    passwords.append(row[1].strip())
                else:
                    print(f"Skipping invalid row: {row}")
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

    return usernames, passwords
