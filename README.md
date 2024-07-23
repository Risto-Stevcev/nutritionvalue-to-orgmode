# nutritionvalue-to-orgmode

`nutritionvalue.org` nutrition calculator CSV to org mode table

## Usage

- Set up script env:

```sh
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip install -r requirements.txt
```

- Go to https://www.nutritionvalue.org/nutritioncalculator.php and type in whatever foods you ate
- Click "Download Spreadsheet (CSV)", this will be the `meal.csv` you pass in:

```
python process.py meal.csv dris.csv | xclip -sel c
```

- Paste it into your org file and press tab next to the top-left corner of the
  table to format it nicely
