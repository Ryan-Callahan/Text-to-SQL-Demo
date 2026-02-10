# Vending Machine Text-to-SQL Project

### Vending Machine DB Schema
![Vending Machine DB](Vending_Machine_Database.png)

This database is intended to track the various kinds of snacks in each vending machine, where
vending machines are located, slot data in each machine, and nutritional info for each snack.

It seems to me that single-domain strategies are often better at generating db-specific sql statements,
while cross-domain tend to generate sql statements that would apply to a more generic database following
common practices. When it comes to the shot count, the higher shot counts tend to be more accurate, but
the differences between them are all very slight.

## Sample Questions

### Correct response
Strategy: zero-shot<br/>
Model: gpt-5.2

Question: <br/>
what kind of snack is the highest carb?

ChatGPT Generated SQL Query: <br/>
```sqlite
SELECT s.name
FROM nutrition n
JOIN snack s ON s.snack_id = n.snack_id
ORDER BY n.total_carbohydrate DESC, s.name
LIMIT 1;
```

Query Result: <br/>
[('Spicy Ramen Cup',)]

ChatGPT Generated Response: <br/>
The snack with the highest carbohydrate content is Spicy Ramen Cup.

### Incorrect response
This question was really close to being correct, and really could be blamed on the fact that
the ingredients list for peanut butter cookies doesn't list nuts, but when compared to the 
single-domain-double-shot version of this same question (which checked ingredients and names)
the resulting query can still be classified as incorrect.

Strategy: cross-domain-quadruple-shot <br/>
Model: gpt-5.2

Question: <br/>
how many items contain any kind of nut?

ChatGPT Generated SQL Query: 
```sqlite
SELECT COUNT(DISTINCT s.snack_id) AS nut_items
FROM snack s
LEFT JOIN nutrition n ON n.snack_id = s.snack_id
WHERE (n.ingredients LIKE '%nut%' OR n.ingredients LIKE '%peanut%' OR n.ingredients LIKE '%almond%' OR n.ingredients LIKE '%cashew%' OR n.ingredients LIKE '%pistachio%' OR n.ingredients LIKE '%hazelnut%' OR n.ingredients LIKE '%walnut%' OR n.ingredients LIKE '%pecan%')
   OR (n.additional_info LIKE '%nut%' OR n.additional_info LIKE '%peanut%' OR n.additional_info LIKE '%almond%' OR n.additional_info LIKE '%cashew%' OR n.additional_info LIKE '%pistachio%' OR n.additional_info LIKE '%hazelnut%' OR n.additional_info LIKE '%walnut%' OR n.additional_info LIKE '%pecan%');
```

Query Result: <br/>
[(10,)]

ChatGPT Generated Response: </br>
10 items contain some kind of nut.

### More Examples

#### Example 1
Strategy: zero-shot <br/>
Model: gpt-5.2

Question: <br/>
how many different juices are there?

ChatGPT Generated SQL Query:

```sqlite
SELECT COUNT(DISTINCT s.snack_id) AS juice_count
FROM snack AS s
WHERE LOWER(s.name) LIKE '%juice%';
```

Query Result: <br/>
[(1,)]

ChatGPT Generated Response: </br>
There is 1 different juice.

#### Example 2
Strategy: single-domain-double-shot <br/>
Model: gpt-5.2

Question: <br/>
how many items contain any kind of nuts?

ChatGPT Generated SQL Query:

```sqlite
SELECT COUNT(DISTINCT s.snack_id)
FROM snack s
LEFT JOIN nutrition n ON n.snack_id = s.snack_id
WHERE LOWER(s.name) LIKE '%nut%'
   OR LOWER(s.name) LIKE '%almond%'
   OR LOWER(s.name) LIKE '%peanut%'
   OR LOWER(s.name) LIKE '%cashew%'
   OR LOWER(s.name) LIKE '%pistachio%'
   OR LOWER(s.name) LIKE '%pecan%'
   OR LOWER(s.name) LIKE '%walnut%'
   OR LOWER(s.name) LIKE '%hazelnut%'
   OR LOWER(s.name) LIKE '%macadamia%'
   OR LOWER(s.name) LIKE '%brazil nut%'
   OR LOWER(n.ingredients) LIKE '%nut%'
   OR LOWER(n.ingredients) LIKE '%almond%'
   OR LOWER(n.ingredients) LIKE '%peanut%'
   OR LOWER(n.ingredients) LIKE '%cashew%'
   OR LOWER(n.ingredients) LIKE '%pistachio%'
   OR LOWER(n.ingredients) LIKE '%pecan%'
   OR LOWER(n.ingredients) LIKE '%walnut%'
   OR LOWER(n.ingredients) LIKE '%hazelnut%'
   OR LOWER(n.ingredients) LIKE '%macadamia%'
   OR LOWER(n.ingredients) LIKE '%brazil nut%';
```

Query Result: <br/>
[(14,)]

ChatGPT Generated Response: </br>
14 items contain some kind of nuts.

#### Example 3
Strategy: zero-shot <br/>
Model: gpt-5.2

Question: <br/>
give me a list of all items that have any kind of tree nut as an ingredient.

ChatGPT Generated SQL Query:

```sqlite
SELECT s.snack_id, s.name
FROM snack AS s
JOIN nutrition AS n ON n.snack_id = s.snack_id
WHERE n.ingredients IS NOT NULL
  AND (
    lower(n.ingredients) LIKE '%almond%'
    OR lower(n.ingredients) LIKE '%almonds%'
    OR lower(n.ingredients) LIKE '%walnut%'
    OR lower(n.ingredients) LIKE '%walnuts%'
    OR lower(n.ingredients) LIKE '%pecan%'
    OR lower(n.ingredients) LIKE '%pecans%'
    OR lower(n.ingredients) LIKE '%cashew%'
    OR lower(n.ingredients) LIKE '%cashews%'
    OR lower(n.ingredients) LIKE '%pistachio%'
    OR lower(n.ingredients) LIKE '%pistachios%'
    OR lower(n.ingredients) LIKE '%hazelnut%'
    OR lower(n.ingredients) LIKE '%hazelnuts%'
    OR lower(n.ingredients) LIKE '%filbert%'
    OR lower(n.ingredients) LIKE '%filberts%'
    OR lower(n.ingredients) LIKE '%brazil nut%'
    OR lower(n.ingredients) LIKE '%brazil nuts%'
    OR lower(n.ingredients) LIKE '%macadamia%'
    OR lower(n.ingredients) LIKE '%macadamias%'
    OR lower(n.ingredients) LIKE '%pine nut%'
    OR lower(n.ingredients) LIKE '%pine nuts%'
    OR lower(n.ingredients) LIKE '%chestnut%'
    OR lower(n.ingredients) LIKE '%chestnuts%'
  );
```

Query Result: <br/>
[]

ChatGPT Generated Response: </br>
No items in the database have any kind of tree nut listed as an ingredient.

#### Example 4
Strategy: zero-shot <br/>
Model: gpt-5.2

Question: <br/>
give me a list of all kinds of bars.

ChatGPT Generated SQL Query:

```sqlite
SELECT DISTINCT s.name
FROM snack AS s
WHERE LOWER(s.name) LIKE '%bar%'
ORDER BY s.name;
```

Query Result: <br/>
[('Chocolate Bar',), ('Granola Bar',), ('Peanut Butter Bar',), ('Peanut Protein Bar',), ('Vegan Bar',)]

ChatGPT Generated Response: </br>
The kinds of bars are Chocolate Bar, Granola Bar, Peanut Butter Bar, Peanut Protein Bar, and Vegan Bar.

#### Example 5
Strategy: single-domain-quadruple-shot <br/>
Model: gpt-5.2

Question: <br/>
how many cookies are in vending machines in the state of utah?

ChatGPT Generated SQL Query:

```sqlite
SELECT COALESCE(SUM(vms.quantity), 0) AS cookies
FROM vending_machine_snack vms
JOIN snack s ON s.snack_id = vms.snack_id
JOIN vending_machine v ON v.machine_id = vms.machine_id
JOIN location l ON l.location_id = v.location_id
WHERE LOWER(l.state) = 'ut'
  AND LOWER(s.name) LIKE '%cookie%';
```

Query Result: <br/>
[(18,)]

ChatGPT Generated Response: </br>
There are 18 cookies in vending machines in the state of Utah.

#### Example 6
Strategy: cross-domain <br/>
Model: gpt-5.2

Question: <br/>
what is the highest protein snack in the state of utah?

ChatGPT Generated SQL Query:

```sqlite
SELECT s.name
FROM snack s
JOIN nutrition n ON n.snack_id = s.snack_id
JOIN vending_machine_snack vms ON vms.snack_id = s.snack_id
JOIN vending_machine vm ON vm.machine_id = vms.machine_id
JOIN location l ON l.location_id = vm.location_id
WHERE UPPER(l.state) = 'UT'
ORDER BY n.protein DESC
LIMIT 1;
```

Query Result: <br/>
[('Beef Jerky',)]

ChatGPT Generated Response: </br>
The highest protein snack in Utah is Beef Jerky.