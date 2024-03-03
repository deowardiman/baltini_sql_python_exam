# Background

(copy and pasted from assignment sheet)
Database
https://t.ly/nOQPE

## Problem Statement
The given SQL file is a database that contains dummy data of our products. We have around
350k products on that sql file. There are many duplicate products from different suppliers
from that collection. We need to merge those duplicate products into one single unique
product, to remove customer confusion and improve the sales metrics.
Similar Product Indicators
- Product ID (available in product tags)
- Gender
- Product Category

## Assignment
1. Create python script to generate product merge suggestions in daily basis, insert a
data to product_duplicates and product_duplicate_details table
2. Create a query to retrieve the list of merge suggestions, please follow the format
below. You can create indexes or partition if necessary to improve the query speed

Group Title Products Count Updated At
XYZ 10 Dec 4, 2023
ABC 5 Dec 6, 2023

# Problem Solving
At the very start of the assignment my main concern is the very definition of "duplicate" products. The assignment sheet has generously enough gave us hint that products with the same "product ID", "gender" and "category" can be considered the same. However such similarities on only those field is not enough, in my opinion, to have 2 or more products be considered the "duplicate". For that reason, I have taken the liberty to add "external_color_code" as the last indicator.

The code that I have written consisted of 4 parts:
1. showing which products that are deemed as duplicates and thus will be removed from "PRODUCTS" table and also how many
2. populating product_duplicates table
3. populating product_duplicate lists
4. finally deleting those porducts that was shown in step 1 from products table

# Running the program
When the program is run, user will be prompted to input 4 things. Those are:
1. host name
2. user
3. password
4. name of the database