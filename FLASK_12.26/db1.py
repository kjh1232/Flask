import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

# conn.execute(
#     '''
#     CREATE TABLE Board (num integer primary key, name TEXT, context TEXT)
#     '''
# )

conn.execute(
    '''
    UPDATE TABLE Board SET Board.num = @CNT:=@CNT+1;
    '''
)


# print ("Table created successfully")

# name = [['Elice', 15], ['Dodo', 16], ['Checher', 17], ['Queen', 18]]
# for i in range(4):
#     conn.execute(f"INSERT INTO Board(name, context) VALUES('{name[i][0]}', '{name[i][1]}')")
conn.commit()
conn.close()