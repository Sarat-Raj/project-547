import os
import requests
from bs4 import BeautifulSoup
import multiprocessing
def pull(year,month):
    # URL of the directory to download files from
    url = "https://www.oakridge.in/wp-content/uploads/"+year+"/"+month+"/"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags that contain links to files
        links = soup.find_all("a")

        # Create a directory to store downloaded files
        download_directory = "downloaded_files"
        os.makedirs(download_directory, exist_ok=True)

        # Loop through the links and download the files
        for link in links:
            href = link.get("href")
            if href and not href.startswith("http"):  # Exclude external links
                file_url = url + href
                file_name = os.path.join(download_directory, os.path.basename(href))

                # Send an HTTP GET request to download the file
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    try:
                        with open(file_name, "wb") as file:
                            file.write(file_response.content)
                        print(f"Downloaded: {file_name}")
                    except: print("fail")
                else:
                    print(f"Failed to download: {file_url}")

    else:
        print(f"Failed to access the URL: {url}")

if __name__=="__main__":
    for x in range(2017,2023,1):
        for y in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            p1 = multiprocessing.Process(target=pull(str(x),str(y)))
            p2 = multiprocessing.Process(target=pull(str(x+1),str(y)))
            p3 = multiprocessing.Process(target=pull(str(x+2),str(y)))
            p1.start()
            p2.start()
            p3.start()
                
        
            