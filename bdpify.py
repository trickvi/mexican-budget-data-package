import unicodecsv as csv
import uuid
import sys
import getopt

# Fields we're interested in and their BDP equivalents
BDP_MAP = {3:'adminID', 4:'admin',
           15:'programID', 16:'program',
           21:'fundID', 22:'fund',
           24:'geocode'}

# Funcational classification (mapped to cofog) is in the following fields
COFOG_FIELDS = (5,7,9)
# Amount is in column 26
AMOUNT = 26

# Read in the mexican functional classification to cofog map
COFOG_MAP = {}

def generate_cofog_map(filename):
    with open(filename) as cofog_map_file:
        reader = csv.reader(cofog_map_file)
        headers = reader.next()
        for row in reader:
            # We join the Mexican classification with dots
            mexican_id = '.'.join(row[:-1])
            COFOG_MAP[mexican_id] = row[-1]

def generate_output_headers():
    # Manual headers we add (or transform existing fields somehow)
    headers = ['id', 'amount', 'cofog', 'functionalID', 'functional']
    # Add other fields ordered by name
    for field_id in sorted(BDP_MAP.keys()):
        headers.append(BDP_MAP[field_id])
    return headers

def output_writer(filename, reader):
    with open(filename, 'w') as output_file:
        writer = csv.writer(output_file)
        # Write the headers
        writer.writerow(generate_output_headers())
        for input_row in reader:
            # Initialize the row with a generated id
            output_row = [uuid.uuid4().hex]
            # Amount is represented with , and . e.g. 4,321.56 but it should
            # just be represented as 4321.56 so we remove the commas.
            output_row.append(float(input_row[AMOUNT].replace(',','')))

            # We need to grab the Mexican functional ids, concatenate them
            # on . (something we chose) and look them up in the cofog map
            # we have generated which will give us the cofog value (next
            # column in the csv)
            mexican_ids = []
            for field in COFOG_FIELDS:
                mexican_ids.append(input_row[field])
            output_row.append(COFOG_MAP['.'.join(mexican_ids)])
            # We also add the Mexican functional classification with the
            # . join we use
            output_row.append('.'.join(mexican_ids))
            # We also join the labels for the Mexican functional
            # classification (this concludes manual additions)
            mexican_label = []
            for field in COFOG_FIELDS:
                mexican_label.append(input_row[field+1])
            output_row.append(' - '.join(mexican_label))

            # Then lastly we add the values of the mapped fields and write
            # out the row to the csv file
            for field_id in sorted(BDP_MAP.keys()):
                output_row.append(input_row[field_id])

            writer.writerow(output_row)


def input_reader(filename):
    with open(filename) as input_file:
        reader = csv.reader(input_file)
        # Ignore header row
        _ign = reader.next()

        for input_row in reader:
            if input_row[-1] == '':
                continue
            yield input_row

def parse_commandline():
    '''
    Parse command line variables
    -m cofog-mapping-file
    -o output-file
    '''
    # Parse commandline using getopts
    myopts, args = getopt.getopt(sys.argv[1:],"o:m:")

    if len(args) != 1:
        print "We only support one argument"
        sys.exit()

    output = {'input': args[0]}
    for option, value in myopts:
        if option == '-o':
            output['output'] = value
        elif option == '-m':
            output['cofog mapping'] = value
    return output

if __name__ == '__main__':
    options = parse_commandline()
    generate_cofog_map(options.get('cofog mapping', 'data/cofog_map.csv'))
    reader = input_reader(options['input'])
    writer = output_writer(options.get('output', 'output.csv'), reader)
