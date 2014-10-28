# Mexican Budget Data Package

Create a Mexican Budget Data Package from a Mexican budget resource file.

## Installing

This is basically just a script but we do use unicodecsv so that we can work
with unicode csv files so we recommend you create a virtualenv and install
unicodecsv via requirements.txt:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Running

To generate a budget data package compatible csv file this just type:

    python bdpify.py -o output.csv -m data/cofog_map.csv input_file.csv

The options default to what was written above so you can also just write:

    python bdpify.py input_file.csv

## License

This software is available under the GNU General Public License, version 3. See LICENCE for more details.