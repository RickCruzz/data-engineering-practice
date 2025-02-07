#%%
import requests
import zipfile
import os

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def unzip_remove(ret, directory, name_file):
    open(f'{directory}/{name_file}.zip', 'wb').write(ret.content)
    
    with zipfile.ZipFile(f'{directory}/{name_file}.zip',"r") as zip_ref:
        zip_ref.extractall(f"{directory}")

    os.remove(f'{directory}/{name_file}.zip')



def main():
    directory = "./downloads"
    os.makedirs(directory, exist_ok=True)
    
    for url in download_uris:
        name_file = url.split("/")[-1]
        ret = requests.get(url)
        if ret.status_code == 200:
            unzip_remove(ret, directory=directory, name_file=name_file)
        else:
            print(f"{ret.status_code} - File Not found check URL: {url}")


if __name__ == "__main__":
    main()
#%%