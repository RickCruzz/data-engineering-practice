
import requests
import pandas as pd
import re
import shutil
import os
import glob

def find_files_by_time(url: str) -> list[str]:
    with requests.get(url, timeout=16) as response:
        pattern = re.compile(r"([A-z0-9]{11}\.csv)")

        s = [
            pattern.search(i)
            for i in response.text.splitlines()
            if re.search(r"2024-01-19 10:27\s{2}", i)
        ]

        return [f"{url}{i.group(0)}" for i in s if i]
    
def download_files_find_max(files_list: list):
    os.makedirs(name="./tmp", exist_ok=True)

    for file in files_list:
        name_file = file.split("/")[-1]
        ret = requests.get(file)
        open(f'./tmp/{name_file}.csv', 'wb').write(ret.content)
    
    folder_path = './tmp/*.csv'
    csv_files = glob.glob(folder_path)
    max_value = 0
    for file in csv_files:
        df = pd.read_csv(file, low_memory=False)
        df_value = float(pd.to_numeric(df["HourlyDryBulbTemperature"].fillna("0"), errors='coerce').max())
        max_value = max(max_value, df_value)
    return max_value



def main():
    url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    file_list = find_files_by_time(url)
    max_value = download_files_find_max(file_list)
    print(max_value)
    shutil.rmtree("./tmp/")


if __name__ == "__main__":
    main()

