# MariaDB SQL Builder

-----

Too lazy to write SQL? Then use the SQL Builder to make your life easier!

MariaDB SQL Builder is a simple and thread safe way to use SQL.
Use your own SQL or use the integrated SQL Builder tool.

## Functions

Currently, the Library can execute the following statements:

**Table**

`Select`, `Update`, `Insert`, `Upsert`, `Delete`

These are also still currently equipped very simple, more functions will be added over time.

**SQL Script**

Perform one or more statements at once.

----

## ! Important !
Keep in mind that as long as a script is executed, one connection is occupied. 
So always consider how many connections you need at startup, changing them later 
is not possible. Connections are only used during an execute/fetch and then released 
again, this process usually does not take long.

----
 
# Setup

## installing

*coming soon*

## Setup

````python
import mariadb_sqlbuilder

connection = mariadb_sqlbuilder.Connect(
    host="HostIP/URL",
    user="User",
    password="Password",
    database="DatabaseToConnect",
    port=3306,  # not required
    pool_name='mypool',  # not required
    pool_size=3,  # not required
    pool_reset_connection=False # not required
    
)
````

With `pool_size` you can set how many connections the library should make (default 3). 
Multiple connections allow multiple simultaneous queries. But more connections need more performance

The connection will always automatically run commit!

## Usage

It is possible to get the sql code, use at the end ``get_sql()`` instead of `execute` or `fetch`.<br>
``get_sql()`` will not use a connection

#### You only want to use SQL Builder and not a connection?

Then do it like this

````python
from mariadb_sqlbuilder.builder import TableBuilder

table = TableBuilder(None, "myTable")  # no connection
# you can use it normal
sql: str = table.insert().set("id", 10).get_sql()

# example for run the sql in your own cursor
cursor.execute(sql)
````

Warning! `execute` and `fetch` will throw errors. 


### Select

Examples for select

```python
# fetch one
result = connection.table("myTable").select("*").fetchone()
# fetch all
result = connection.table("myTable").select("*").fetchall()

# Select specific column/s
result = connection.table("myTable").select("id").fetchall()
result = connection.table("myTable").select("id, name, age, email").fetchall()

# Select something with where
result = connection.table("myTable").select("name, age, email").where("age", 25).fetchall()
# Multiple where
result = connection.table("myTable").select("name, age, email").where("age", 25).where("name", "Helgo").fetchall()
```

The result is the same as a normal sql execute

### Update

Examples for Update

```python
# update all
result = connection.table("myTable").update().set("age", 25).execute()
# update multiple
result = connection.table("myTable").update().set("age", 25).set("name", "Helgo").execute()

# update with where statements
result = connection.table("myTable").update().set("age", 25).where("id", 10).execute()

```

### Insert

Examples for Insert

```python
# normal insert
result = connection.table("myTable").insert().set("id", 10).set("age", 25).set("Name", "Helgo").execute()
# insert ignore
result = connection.table("myTable").insert().set("id", 10).ignore().execute()

```

### Upsert

Examples for Upsert

What is Upsert? Upsert is an Insert with Update when a key is duplicated

```python
# upsert
result = connection.table("myTable").upsert().set("id", 10).set("name", "Helgo").execute()
# this will update the row before
result = connection.table("myTable").upsert().set("id", 10).set("name", "Helgo the Hero").execute()
```

### Delete

Examples for Delete something

```python
# delete with where
result = connection.table("myTable").delete().where("id", 10).execute()

# delete without where is not possible on this way, it wil throws an error
result = connection.table("myTable").delete().execute()
# if you really want to delete all data in a table use this way
# the true is important, otherwise it will also throw an error
result = connection.table("myTable").delete().imSureImNotUseWhere(True).execute()
# but you can still get the sql this way
result = connection.table("myTable").delete().get_sql()
```

Translated with www.DeepL.com/Translator (free version)