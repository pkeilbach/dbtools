from dbtools import MySql


credentials = {
    'user': 'user',
    'password': 'password',
}


with MySql(**credentials) as cnx:
    query = "SELECT * FROM my_table WHERE my_id = %(my_id)s"
    df = cnx.select(query, params={'my_id': 17}, return_df=True)
    print(df)

    query = "SELECT * FROM my_table WHERE my_id = 17"
    s = cnx.select(query, fetchone=True, dictionary=True)
    print(s)

print('success')
