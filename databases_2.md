
# Базы данных. Часть 2

## Базы данных и Python

Питон позволяет работать с различными СУБД, но проще всего использовать встроенную библиотеку [SQLite](https://docs.python.org/3.5/library/sqlite3.html). Важно также запомнить, что файлы баз данных имеют расширение `.db`.


```python
import sqlite3

# подключаемся к базе данных
conn = sqlite3.connect('example2.db')
```

**Важная вещь №1**: после подключения к БД нужно обязательно инициализировать курсор, иначе вы не сможете делать к ней запросы!


```python
# создаем объект "курсор", которому будем передавать запросы
c = conn.cursor()

# создаем таблицу
c.execute("CREATE TABLE IF NOT EXISTS students(name text, major text, year integer)")

# вставляем строку
c.execute("INSERT INTO students VALUES ('Петя','филология',1), ('Настя','лингвистика',4)")

# сохраняем изменения
conn.commit()

# отключаемся от БД
#conn.close()
```

**Важная вещь №2**: если вы что-то изменили, нужно обязательно закоммитить изменения, иначе они не сохранятся в файле БД!

Когда вы создали базу данных и ее закоммитили, вы можете открыть её через DBrowser (flashback прошлый семинар) и проверить правильно ли она у вас создалась.

**И немного о безопасности**: при создании запроса нельзя использовать конкатенацию строк и форматирование строк, как в питоне. Это сделает ваше приложение уязвимым для SQL-инъекций - особых хакерских атак, которые заключаются в подставлении в запрос нежелательных комманд - например, DROP TABLE. Поподробнее об этом можно почитать [вот здесь](https://habrahabr.ru/post/148151/).

![](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)


```python
# Так нельзя!
name = 'Петя'
c.execute("SELECT * FROM students WHERE name = '%s'" % name)

# Вот как надо
x = ('Петя',)
c.execute('SELECT * FROM students WHERE name=?', x)
print(c.fetchone())
```

    ('Петя', 'филология', 1)
    


```python
# Если результатом запроса является несколько строк, можно по ним итерировать

for row in c.execute('SELECT * FROM students ORDER BY year'):
    print(row)
```

    ('Петя', 'филология', 1)
    ('Настя', 'лингвистика', 4)
    


```python
# как подставить несколько переменных в sql-запрос

x = 'Аня'
y = 'математика'
z = 3

c.execute('INSERT INTO students VALUES (?, ?, ?)', (x, y, z))
conn.commit()
```

#### Форматирование строк

Если нужно подставить переменные в качестве названия таблицы или колонок, то придется использовать форматирование строк.


```python
params = ['vowel', 'f1', 'f2']
c.execute('CREATE TABLE vowels({}, {}, {})'.format(params[0], params[1], params[2]))
```




    <sqlite3.Cursor at 0x4dc67a0>




```python
# как написать длинный запрос посимпатичнее
c.execute('''
INSERT INTO vowels 
VALUES 
('a', 1234.56, 4567.8), 
('u', 1111.1, 3333.3)'''
)
```




    <sqlite3.Cursor at 0x4dc67a0>




```python
for row in c.execute('SELECT * FROM vowels'):
    print(row)
```

    ('a', 1234.56, 4567.8)
    ('u', 1111.1, 3333.3)
    

#### Функции курсора

* **fetchone()** -- возвращает следующий элемент из результата запроса (т.е. одну строку из бд). Результат -- кортеж, где элементом является значение каждой из колонок или None
* **fetchall()** -- возвращает все результаты запроса в виде списка
* **fetchmany()** -- возвращает заданное количество строк из результатов запроса


```python
# извлекаем строки по одной
# обратите внимание, что после каждого вызова fetchone возвращает следующую строку!
c.execute('SELECT * FROM students ORDER BY year')
print(c.fetchone())
print(c.fetchone())
print(c.fetchone())
```

    ('Петя', 'филология', 1)
    ('Аня', 'математика', 3)
    ('Настя', 'лингвистика', 4)
    


```python
# извлекаем две строки
c.execute('SELECT * FROM students ORDER BY year')
print(c.fetchmany(2))
```

    [('Петя', 'филология', 1), ('Аня', 'математика', 3)]
    


```python
# извлекаем все строки
c.execute('SELECT * FROM students ORDER BY year')
print(c.fetchall())
```

    [('Петя', 'филология', 1), ('Аня', 'математика', 3), ('Настя', 'лингвистика', 4)]
    


```python
# Не забудьте отключить от бд, чтобы не тратить память :)
conn.close()
```

# Практика

* Прочитайте таблицу из файла `rutul_vowels.csv` (находится в папке с семинаром) в датафрейм и посмотрите с помощью .head(), что там вообще за колонки. Или можете просто посмотреть, что это за таблица в notepad++ у себя на компе

Записать данные из файла в новую базу данных можно двумя способами:

1. модуль csv и метод `csv.DictReader()`. Создайте новую базу данных и создайте в этой базе данных новую таблицу с колонками, соответствующими колонкам в rutul_vowels. Прочитать файл и построчно записать всё в базу данных с помощью `c.executemany()`
2. В модуле pandas есть функция `df.to_sql()`. Тут нужно только создать новый connection и новый cursor. Самостоятельно делать CREATE новой таблицы с правильными названиями всех колонок - не надо! В целом этот способо в сто раз круче.

### Ответ


```python
import pandas as pd
import csv
import sqlite3
```


```python
df = pd.read_csv('rutul_vowels.csv', sep=',', encoding='utf-8')
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>word</th>
      <th>translation</th>
      <th>vowel</th>
      <th>stress</th>
      <th>syllable</th>
      <th>left_context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>χed</td>
      <td>дикая алыча</td>
      <td>e</td>
      <td>yes</td>
      <td>cvc</td>
      <td>χ</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>eked</td>
      <td>старший</td>
      <td>e</td>
      <td>no</td>
      <td>cv</td>
      <td>no</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ɢina</td>
      <td>в Кинe</td>
      <td>i</td>
      <td>yes</td>
      <td>cv</td>
      <td>ɢ</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>χuda</td>
      <td>в кулаке</td>
      <td>u</td>
      <td>no</td>
      <td>cv</td>
      <td>χ</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>ʁuli</td>
      <td>в окне</td>
      <td>u</td>
      <td>no</td>
      <td>cv</td>
      <td>ʁ</td>
    </tr>
  </tbody>
</table>
</div>




```python
con = sqlite3.connect("rutul.db")
cur = con.cursor()
```

Воспользуемся вторым, более клёвым способом:


```python
df.to_sql(name='rutul', con=con, if_exists='replace')
```

Проверим, что таблица базы данных созадалась:

(Либо можно открыть в DBrowser и поглядеть там, что всё нормально)


```python
for row in cur.execute('SELECT * FROM rutul'):
    print(row)
```

    (0, 1, 'χed', 'дикая алыча', 'e', 'yes', 'cvc', 'χ')
    (1, 2, 'eked', 'старший', 'e', 'no', 'cv', 'no')
    (2, 3, 'ɢina', 'в Кинe', 'i', 'yes', 'cv', 'ɢ')
    (3, 4, 'χuda', 'в кулаке', 'u', 'no', 'cv', 'χ')
    (4, 5, 'ʁuli', 'в окне', 'u', 'no', 'cv', 'ʁ')
    (5, 6, 'ɢuje', 'в яме', 'u', 'yes', 'cv', 'ɢ')
    (6, 7, 'qaka', 'отдай назад', 'a', 'yes', 'cv', 'q')
    (7, 8, 'qiq’a', 'возвращайся', 'i', 'yes', 'cv', 'q')
    (8, 9, 'χɨd', 'липа', 'ɨ', 'yes', 'cvc', 'χ')
    (9, 10, 'ʁɨˁbar', 'лягушки', 'ɨˁ', 'no', 'cv', 'ʁ')
    (10, 11, 'χaˁrad', 'масло', 'aˁ', 'no', 'cv', 'χ')
    (11, 12, 'itɨd', 'медовый', 'i', 'yes', 'cv', 'no')
    (12, 13, 'uˁbra', 'мерка для муки', 'uˁ', 'no', 'cv', 'no')
    


```python
import sqlite3
import csv
con = sqlite3.connect("rutul3.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS rutul3")
cur.execute("CREATE TABLE rutul3 (vowel, translation, syllable);")  # тут надо аккуратно переписать названия всех колонок

with open('rutul_vowels.csv','r', encoding='utf-8') as fin:
    dr = csv.DictReader(fin)  # запятая является разделителем по умолчанию
    to_db = [(i['vowel'], i['translation'], i['syllable']) for i in dr]  # снова переписать имена колонок

cur.executemany("INSERT INTO rutul3 (vowel,translation, syllable) VALUES (?, ?, ?);", to_db)  # и снова переписать имена колонок

for i in cur.execute("SELECT * FROM rutul3"):
    print(i)
    
con.commit()
con.close()
```

    ('e', 'дикая алыча', 'cvc')
    ('e', 'старший', 'cv')
    ('i', 'в Кинe', 'cv')
    ('u', 'в кулаке', 'cv')
    ('u', 'в окне', 'cv')
    ('u', 'в яме', 'cv')
    ('a', 'отдай назад', 'cv')
    ('i', 'возвращайся', 'cv')
    ('ɨ', 'липа', 'cvc')
    ('ɨˁ', 'лягушки', 'cv')
    ('aˁ', 'масло', 'cv')
    ('i', 'медовый', 'cv')
    ('uˁ', 'мерка для муки', 'cv')
    


```python
import sqlite3

with open('rutul_vowels.csv', 'r', encoding='utf-8') as f:
    f = f.readlines()

# подключаемся к базе данных
conn = sqlite3.connect('rutul2.db')

# создаем объект "курсор", которому будем передавать запросы
c = conn.cursor()

# создаем таблицу
c.execute("DROP TABLE IF EXISTS rutul")
c.execute("CREATE TABLE IF NOT EXISTS rutul(id,word,translation,vowel,stress,syllable)")

for row in f:
    row = row.split(',')
    c.execute("INSERT INTO rutul VALUES (?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5]))

# сохраняем изменения
conn.commit()

for i in c.execute("SELECT * FROM rutul WHERE vowel='ɨˁ' AND stress='no' AND syllable='cv'"):
    print(i)

# отключаемся от БД
conn.close()
```

    ('10', 'ʁɨˁbar', 'лягушки', 'ɨˁ', 'no', 'cv')
    

### Вторая часть этого задания на составление запросов

Теперь можно написать какие-нибудь запросы к созданной базе данных.

* Распечатайте все слова, в которых целевая гласная находится в безударной позиции
* Распечатайте все слова, в которых целевая гласная в безударной позиции и нет левого контекста


```python
# Тут нужно писать запросы к получившейся базе
cur.execute('SELECT * FROM rutul WHERE stress="no"')
print(cur.fetchall())

```

    [(1, 2, 'eked', 'старший', 'e', 'no', 'cv', 'no'), (3, 4, 'χuda', 'в кулаке', 'u', 'no', 'cv', 'χ'), (4, 5, 'ʁuli', 'в окне', 'u', 'no', 'cv', 'ʁ'), (9, 10, 'ʁɨˁbar', 'лягушки', 'ɨˁ', 'no', 'cv', 'ʁ'), (10, 11, 'χaˁrad', 'масло', 'aˁ', 'no', 'cv', 'χ'), (12, 13, 'uˁbra', 'мерка для муки', 'uˁ', 'no', 'cv', 'no')]
    


```python
cur.execute('SELECT * FROM rutul WHERE stress="no" AND left_context="no"')
print(cur.fetchall())
```

    [(1, 2, 'eked', 'старший', 'e', 'no', 'cv', 'no'), (12, 13, 'uˁbra', 'мерка для муки', 'uˁ', 'no', 'cv', 'no')]
    


```python
# Не забыть!
con.close()
```
