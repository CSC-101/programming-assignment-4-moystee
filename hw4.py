import sys
import json

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print("Error: Cannot open file {}.".format(file_path))
        sys.exit(1)
def display(data):
    for county in data:
        print("County: {}, State: {}, Population: {}, Education (Bachelor's Degree or Higher): {}".format(
            county['County'], county['State'], county['Population'], county["Education.Bachelor's Degree or Higher"]))
def filter_state(data, state):
    filtered_data = [county for county in data if county['State'] == state]
    print("Filter: state == {} ({} entries)".format(state, len(filtered_data)))
    return filtered_data
def filter_gt(data, field, number):
    filtered_data = [county for county in data if float(county[field]) > number]
    print("Filter: {} gt {} ({} entries)".format(field, number, len(filtered_data)))
    return filtered_data
def filter_lt(data, field, number):
    filtered_data = [county for county in data if float(county[field]) < number]
    print("Filter: {} lt {} ({} entries)".format(field, number, len(filtered_data)))
    return filtered_data
def population_total(data):
    total_population = sum(county['Population'] for county in data)
    print("2014 population: {}".format(total_population))
def population_field(data, field):
    total_population = sum(county['Population'] for county in data)
    field_population = sum(county['Population'] * float(county[field]) / 100 for county in data)
    print("2014 {} population: {}".format(field, field_population))
def percent_field(data, field):
    total_population = sum(county['Population'] for county in data)
    field_population = sum(county['Population'] * float(county[field]) / 100 for county in data)
    if total_population > 0:
        percentage = (field_population / total_population) * 100
        print("2014 {} percentage: {}".format(field, percentage))
    else:
        print("2014 {} percentage: 0".format(field))
def process_operations(data, operations_file):
    with open(operations_file, 'r') as file:
        line_number = 0
        for line in file:
            line_number += 1
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            try:
                parts = line.split(':')
                command = parts[0]

                if command == 'display':
                    display(data)
                elif command.startswith('filter-state'):
                    state = parts[1]
                    data = filter_state(data, state)
                elif command.startswith('filter-gt'):
                    field = parts[1]
                    number = float(parts[2])
                    data = filter_gt(data, field, number)
                elif command.startswith('filter-lt'):
                    field = parts[1]
                    number = float(parts[2])
                    data = filter_lt(data, field, number)
                elif command == 'population-total':
                    population_total(data)
                elif command.startswith('population'):
                    field = parts[1]
                    population_field(data, field)
                elif command.startswith('percent'):
                    field = parts[1]
                    percent_field(data, field)
                else:
                    print("Error: Invalid operation at line {}.".format(line_number))
            except Exception as e:
                print("Error: Malformed operation at line {}. {}".format(line_number, str(e)))

def main():
    if len(sys.argv) != 2:
        print("Error: Please provide the operations file as a command-line argument.")
        sys.exit(1)
    operations_file = sys.argv[1]
    data = load_data("counties_demographics.json")
    print("Loaded {} entries.".format(len(data)))
    process_operations(data, operations_file)

if __name__ == "__main__":
    main()