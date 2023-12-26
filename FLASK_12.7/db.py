import sqlite3

conn = sqlite3.connect('member.db')
print('create & connect database')

# conn.execute(
#     '''
#     create table member (id text, pwd text)
#     '''
# )


# conn.execute(
#     '''
#     insert into member(id, pwd) values('minji', '4567')
#     '''
# )

conn.execute(
    '''
    insert into member(id, pwd) values('jihee', '1234')
    '''
)

conn.commit()
print('insert table')

conn.close()