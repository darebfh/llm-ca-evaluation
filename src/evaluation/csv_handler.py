import csv


class CSVHandler:
    @staticmethod
    def read_csv(file_path):
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            # Process and return the data as needed
            data = [row for row in reader]
        return data

    @staticmethod
    def write_to_csv(file_path, data, header=None):
        """
        Write data to a CSV file.

        Parameters:
        - file_path (str): The path to the CSV file.
        - data (list of lists): The data to be written to the CSV file. Each inner list represents a row.
        - header (list, optional): The header row of the CSV file. If not provided, no header will be written.

        Example usage:
        write_to_csv('output.csv', [['Name', 'Age', 'City'], ['John', 25, 'New York'], ['Jane', 30, 'Los Angeles']], header=True)
        """
        with open(file_path, "w", newline="") as file:
            csv_writer = csv.writer(file)

            # Write the header if provided
            if header:
                csv_writer.writerow(header)

            # Write the data
            csv_writer.writerows(data)
