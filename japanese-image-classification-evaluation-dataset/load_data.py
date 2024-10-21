import csv
import pickle as pkl
import os
import random
import time
from urllib.request import urlretrieve

random.seed(42)

def image_to_binary(image_path):
    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()
    return binary_data

def get_csv_files(directory):
    csv_files = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            csv_files.append(file)
    return csv_files

def read_csv_data(file_path):
    file_name = os.path.basename(file_path).split('.')[0]
    if 'flower' in file_name:
        category = 'flower'
    elif 'food' in file_name:
        category = 'food'
    elif 'facility' in file_name:
        category = 'facility'
    elif 'landmark' in file_name:
        category = 'landmark'
    
    data  = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)
        random.shuffle(rows)
        for i, row in enumerate(rows[:0]):
            id_ = row[0]
            url = row[3]
            label = row[4]
            image_file = os.path.join('images', file_name, f'{id_}.jpg')
            if not os.path.exists(image_file):
                urlretrieve(url, image_file)
                time.sleep(1.0)
            image_binary = image_to_binary(image_file)
            data.append((image_binary, label, category))
    
    return data


if __name__ == "__main__":
    file_paths = get_csv_files('.')
    full_data = {'image': [], 'label': [], 'category': []}
    for f in file_paths:
        data = read_csv_data(f)
        for d in data:
            full_data['image'].append(d[0])
            full_data['label'].append(d[1])
            full_data['category'].append(d[2])
    with open('eval_data.pkl', 'wb') as file:
        pkl.dump(full_data, file)