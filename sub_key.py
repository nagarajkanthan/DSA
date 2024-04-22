import json
import csv

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def compare_nested_keys(json1, json2, parent_key=''):
    compared_data = []
    for key in json1.keys():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if key in json2:
            val1 = json1[key]
            val2 = json2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                compared_data.extend(compare_nested_keys(val1, val2, full_key))
            else:
                if val1 == val2:
                    comparison = 'Match'
                else:
                    comparison = 'Mismatch'
                compared_data.append({'Key': full_key, 'Value in File 1': val1, 'Value in File 2': val2, 'Comparison': comparison})
        else:
            compared_data.append({'Key': full_key, 'Value in File 1': json1[key], 'Value in File 2': None, 'Comparison': 'Key only in File 1'})
    for key in json2.keys():
        if key not in json1:
            compared_data.append({'Key': key, 'Value in File 1': None, 'Value in File 2': json2[key], 'Comparison': 'Key only in File 2'})
    return compared_data

def write_comparison_to_csv(compared_data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Key', 'Value in File 1', 'Value in File 2', 'Comparison'])
        writer.writeheader()
        writer.writerows(compared_data)

if __name__ == '__main__':
    json_file1 = r'C:\Users\nagar\OneDrive\Desktop\testing_data\golden.json'
    json_file2 = r'C:\Users\nagar\OneDrive\Desktop\testing_data\user.json'
    output_csv_file = 'comparison_results.csv'

    json_data1 = load_json(json_file1)
    json_data2 = load_json(json_file2)

    compared_data = compare_nested_keys(json_data1, json_data2)

    write_comparison_to_csv(compared_data, output_csv_file)