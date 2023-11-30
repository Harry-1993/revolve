import argparse
import os
import json
from typing import List, Dict

def read_csv(file_path: str) -> List[Dict]:
    # Function to read CSV files and return a list of dictionaries
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []

    # Assuming the first line contains headers
    if not lines or len(lines) < 2:
        print(f"Error: Empty or invalid CSV file - {file_path}")
        return []

    headers = lines[0].strip().split(',')
    data = []

    for line in lines[1:]:
        values = line.strip().split(',')

        # Skip empty lines
        if not any(values):
            continue

        # Check if the lengths of headers and values are the same
        if len(headers) != len(values):
            print(f"Error: Inconsistent number of columns in CSV file - {file_path}")
            print(f"Headers: {headers}")
            print(f"Values: {values}")
            return []

        row = {headers[i]: values[i] for i in range(len(headers))}
        data.append(row)

    return data

def read_json_lines(folder_path: str) -> List[Dict]:
    # Function to read JSON Lines files from a folder and return a list of dictionaries
    data = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"Error: Folder not found - {folder_path}")
    return data

def process_data(customers: List[Dict], transactions: List[Dict], products: List[Dict]) -> List[Dict]:
    # Function to process data and generate the required output
    output_data = []
    customer_dict = {customer['customer_id']: {'loyalty_score': customer['loyalty_score']} for customer in customers}

    for transaction in transactions:
        customer_id = transaction['customer_id']
        basket = transaction['basket']

        # Initialize purchase count for the customer
        if 'purchase_count' not in customer_dict[customer_id]:
            customer_dict[customer_id]['purchase_count'] = 0

        for item in basket:
            product_id = item['product_id']
            price = item['price']

            # Initialize product category in the customer dictionary
            if 'product_categories' not in customer_dict[customer_id]:
                customer_dict[customer_id]['product_categories'] = {}

            # Increment purchase count and update product category information
            customer_dict[customer_id]['purchase_count'] += 1
            if product_id not in customer_dict[customer_id]['product_categories']:
                product_category = next((product['product_category'] for product in products if product['product_id'] == product_id), None)
                customer_dict[customer_id]['product_categories'][product_id] = product_category

    # Convert the processed dictionary into a list for output
    for customer_id, customer_data in customer_dict.items():
        output_data.append({
            'customer_id': customer_id,
            'loyalty_score': customer_data['loyalty_score'],
            'product_id': list(customer_data['product_categories'].keys()),
            'product_category': list(customer_data['product_categories'].values()),
            'purchase_count': customer_data['purchase_count']
        })

    return output_data

def write_output(output_data: List[Dict], output_location: str) -> None:
    # Function to write the processed data to a JSON file

    # Ensure the output directory exists
    os.makedirs(output_location, exist_ok=True)

    output_file_path = os.path.join(output_location, 'output.json')
    try:
        with open(output_file_path, 'w') as file:
            json.dump(output_data, file, indent=2)
    except IOError:
        print(f"Error: Unable to write to the output file - {output_file_path}")

def get_params() -> dict:
    parser = argparse.ArgumentParser(description='DataTest')
    parser.add_argument('--customers_location', required=False, default="../input_data/starter/customers.csv")
    parser.add_argument('--products_location', required=False, default="../input_data/starter/products.csv")
    parser.add_argument('--transactions_location', required=False, default="../input_data/starter/transactions/")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    return vars(parser.parse_args())

def main():
    params = get_params()

    # Read data from CSV and JSON sources
    customers = read_csv(params['customers_location'])
    products = read_csv(params['products_location'])

    if not customers or not products:
        print("Error: Unable to read necessary input files. Exiting.")
        return

    # Process data
    transactions = read_json_lines(params['transactions_location'])

    if not transactions:
        print("Error: Unable to read transactions. Exiting.")
        return

    output_data = process_data(customers, transactions, products)

    # Write output to JSON file
    write_output(output_data, params['output_location'])

if __name__ == "__main__":
    main()
