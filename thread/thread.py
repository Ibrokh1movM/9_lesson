import threading
import requests
import json


def fetch_data_and_save_to_json(url, filename):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(filename, 'w') as json_file:
                json.dump(response.json(), json_file, indent=4)
            print(f"Data from {url} saved to {filename}")
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_and_save_first_url():
    url = "https://dummyjson.com/products"
    filename = "products_data.json"
    fetch_data_and_save_to_json(url, filename)


def fetch_and_save_second_url():
    url = "https://jsonplaceholder.typicode.com/posts"
    filename = "posts_data.json"
    fetch_data_and_save_to_json(url, filename)


if __name__ == "__main__":
    thread1 = threading.Thread(target=fetch_and_save_first_url)
    thread2 = threading.Thread(target=fetch_and_save_second_url)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both threads have finished their tasks.")
