import pandas as pd
import glob
import os

file_pattern = "data_*.xlsx"
data_frames = []
for file_path in glob.glob(file_pattern):
    file_name = os.path.basename(file_path)
    parts = file_name.split('_')
    if len(parts) >= 3:
        try:
            year = int(parts[1])
            month_str = parts[2].split('.')[0]
            if len(month_str) == 2 and month_str.isdigit():
                month = int(month_str)
            else:
                print(f"Ошибка: Месяц в имени файла '{file_name}' некорректен.")
                continue
        except ValueError as e:
            print(f"Ошибка при обработке файла '{file_name}': {e}")
            continue
    else:
        print(f"Ошибка: Имя файла '{file_name}' не соответствует ожидаемому формату.")
        continue

    try:
        data = pd.read_excel(file_path, skiprows=5)
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_name}': {e}")
        continue

    index_cut = data[data.iloc[:, 0] == "Чукотский автономный округ"].index
    if not index_cut.empty:
        data = data.loc[:index_cut[0]]

    data["Год"] = year
    data["Месяц"] = month
    data_frames.append(data)

if data_frames:
    final_data = pd.concat(data_frames, ignore_index=True)
    final_data.to_excel("datatest.xlsx", index=False)
    print('1')



