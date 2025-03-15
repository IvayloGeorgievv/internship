import csv
import os

def generate_csv(filename, data, directory='data'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if data:
            # Write header
            writer.writerow(data[0].keys())
            # Write each row after cleaning newline characters from each field
            for row in data:
                clean_row = [str(value).replace('\n', ' ').replace('\r', ' ') for value in row.values()]
                writer.writerow(clean_row)

    print(f"{filename} generated successfully with {len(data)} records")
