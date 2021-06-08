# DBTools

This Python package is designed to provide easy access to MySQL databases

## Installation

```sh
# TODO
```

## Usage

```python
from dbtools import MySql

credentials = {
    'user': 'user',
    'password': 'password',
}


with MySql(**credentials) as cnx:
    stmt = "SELECT * FROM my_table WHERE my_id = %(my_id)s"
    params={'my_id': 17}
    
    # select returns a df by default or a list of dicts otherwise
    df = cnx.select(stmt, params=params, return_df=True)
    
    # use the execute methods to execute all kinds of queries
    s = cnx.select(stmt)

```
