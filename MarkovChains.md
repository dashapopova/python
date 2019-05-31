

```python
import pandas as pd

provs = pd.read_csv('dal_proverbs.csv', sep='\t', encoding='utf-8')
provs.head()
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
      <th>proverb</th>
      <th>topic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Жить — богу служить.</td>
      <td>Бог — Вера</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Кто велик, яко бог наш (Влад. Моном.).</td>
      <td>Бог — Вера</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Не нам, не нам, но имени твоему (т. е. слава).</td>
      <td>Бог — Вера</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Велико имя господне на земли.</td>
      <td>Бог — Вера</td>
    </tr>
    <tr>
      <th>4</th>
      <td>В мале бог, и в велике бог.</td>
      <td>Бог — Вера</td>
    </tr>
  </tbody>
</table>
</div>




```python
shuffled = provs.sample(frac=1)
train = ' '.join(shuffled.proverb)
train[:200]
```




    'Не диковина, что кукушка в чужое гнездо полезла, а вот то б  диковина, кабы свое свила. Он сам своей тени боится. Нырять он умеет, только выныривать не умеет. Обойдешь да огладишь, так и на строгого к'




```python
import markovify

m = markovify.Text(train)
```


```python
for i in range(5):
    print(m.make_sentence())
```

    Год не неделя, а все лучше худого ворчанья.
    Удалой долго не растает.
    Дай прокормить казенного воробья — без рубахи пойду, а тебя по смерть посылать.
    Не жилой — не косить, спина не болит.
    Ныне не спрашивай старого, спрашивай бывалого.
    


```python
for i in range(5):
    print(m.make_short_sentence(max_chars=100))
```

    Наг поле перейдет, а наг — ни в масленицу, а привел бог в господина и жить добро.
    Плохой то вор, что хорошо крадет, а под старость в монахи пошел.
    Ах, мак, да бояре едят.
    Люби ссору, люби и отдать.
    Старинная пословица не для прибыли, а для единого единства и дружного компанства.
    
