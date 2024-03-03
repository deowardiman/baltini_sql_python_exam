import mysql.connector

host=input('Please input host ')
user = input('Please input user ')
passwd = input('Please input password ')
database = input('Please input the name of the database ')

db=mysql.connector.connect(
    host=host,
    user = user,
    passwd = passwd,
    database = database
)

c=db.cursor()



#show product merge suggestion
suggest = """
select concat(coalesce(title,''), coalesce(external_product_code,''), coalesce(gender,''), coalesce(category,''), coalesce(external_color_code,'')) as col1, jumlah, now() from (
SELECT group_concat(distinct title order by title) title, external_product_code, gender, category, external_color_code, count(1) jumlah
FROM {db}.products group by external_product_code, gender, category, external_color_code having(jumlah)>1 order by title asc
) dup;
""".format(db=database)
c.execute(suggest)

data = c.fetchall()

for e in data:
    print(e)


#populate product_duplicates table
duplicates = """
insert into {db}.product_duplicates (title, created_at, updated_at)
select concat(coalesce(title,''), coalesce(external_product_code,''), coalesce(gender,''), coalesce(category,''), coalesce(external_color_code,'')), now() as created_at, now() as updated_at from
(SELECT group_concat(distinct title order by title) as title, external_product_code, gender, category, external_color_code, count(1) jumlah
FROM {db}.products group by external_product_code, gender, category, external_color_code having(jumlah)>1 order by jumlah asc) a;
""".format(db=database)

c.execute(duplicates)

print("populate product_duplicates table done")

#populate product_duplicate_lists table
duplicate_list ="""
insert into {db}.product_duplicate_lists (product_duplicate_id, external_id, product_id, deleted_at, created_at, updated_at)
select duplicates.id, b.external_product_code, b.id as product_id, now() as deleted_at, now() as created_at, now() as updated_at from (
select dups.*, dup_list.col1 from (
SELECT id, title, external_product_code, gender, category, external_color_code, external_id,
count(1) over (partition by external_product_code, gender, category, external_color_code) jumlah,
rank() over (partition by external_product_code, gender, category, external_color_code order by id) ranking
FROM {db}.products) dups
join 
(select dup.*, concat(coalesce(title,''), coalesce(external_product_code,''), coalesce(gender,''), coalesce(category,''), coalesce(external_color_code,'')) as col1 from (
SELECT group_concat(distinct title order by title) title, external_product_code, gender, category, external_color_code, count(1) jumlah
FROM {db}.products group by external_product_code, gender, category, external_color_code having(jumlah)>1 order by title asc
) dup) dup_list on dup_list.external_product_code = dups.external_product_code and
dup_list.gender = dups.gender and
dup_list.category = dups.category and
dup_list.external_color_code = dups.external_color_code
where dups.jumlah>1 and ranking != 1
) b
join {db}.product_duplicates duplicates on b.col1 = duplicates.title;
""".format(db=database)
c.execute(duplicate_list)

print("populate product_duplicate_lists table done")

#delete from products table
delete_product = """
delete from products where id in (
select id from (
SELECT id, title, external_product_code, gender, category, external_color_code, external_id,
count(1) over (partition by external_product_code, gender, category, external_color_code) jumlah,
rank() over (partition by external_product_code, gender, category, external_color_code order by id) ranking
FROM {db}.products) dups
join 
(select dup.*, concat(coalesce(title,''), coalesce(external_product_code,''), coalesce(gender,''), coalesce(category,''), coalesce(external_color_code,'')) as col1 from (
SELECT group_concat(distinct title order by title) title, external_product_code, gender, category, external_color_code, count(1) jumlah
FROM {db}.products group by external_product_code, gender, category, external_color_code having(jumlah)>1 order by title asc
) dup) dup_list on dup_list.external_product_code = dups.external_product_code and
dup_list.gender = dups.gender and
dup_list.category = dups.category and
dup_list.external_color_code = dups.external_color_code
where dups.jumlah>1 and ranking != 1
)"""

c.execute(delete_product)
print("delete from products table done")

db.close