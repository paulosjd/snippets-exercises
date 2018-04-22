Indexing
========
![](../images/b-tree.png)

In its most basic form, the B-Tree index is a hierarchy of data pages. The lowest level is called the leaf level, the highest level is the index root, and all levels in between are the intermediate levels. This structure is an improvement over the Binary Tree index because its balanced nature greatly improved the performance of maintenance operations such as, `INSERT`, `DELETE`, and `UPDATE`.
All table data is stored in 8 KB data pages. The data pages are at the leaf level.

B Tree Index:
This is the default index for most of the storage engines in MySQL.The general idea of a B-Tree is that all the values are stored in order, and each leaf page is the same distance from the root.B Tree index speeds up the data access because storage engine don't have to scan the whole table instead it will start from root node. The slots in the root node hold pointers to child nodes, and the storage engine follows these pointers. It finds the right pointer by looking at the values in the node pages, which define the upper and lower bounds of the values in the child nodes. Eventually, the storage engine either determines that the desired value doesn't exist or successfully reaches a leaf page. Leaf pages are special, because they have pointers to the indexed data instead of pointers to other pages.

You add indexes on columns when you want to speed up searches on that column. Typically, only the primary key is indexed by the database. This means look ups using the primary key are optimized.

If you do a lot of lookups on a secondary column, consider adding an index to that column to speed things up.
Keep in mind, like most problems of scale, these only apply if you have a statistically large number of rows (10,000 is not large).

Remember when you add additional indexes, Read operations get faster but Write operations becomes slower because of recalculation of the indexes. So use them as per your use case demands.
When choosing to index a key, consider whether the performance gain for queries is worth the performance loss for INSERTs, UPDATEs, and DELETEs and the use of the space required to store the index. As always, you can only optimize what you can measure (e.g. with Django Debug Toolbar). Some general points to consider are:

    - Consider indexing keys that are used frequently in WHERE clauses.
    - Consider indexing keys that are used frequently to join tables in SQL statements.
    - Choose index keys that have high selectivity. An index's selectivity is optimal if few rows have the same value.
    - It follows: Do not use standard B-tree indexes on keys or expressions with few distinct values
    - Do not index columns that are modified frequently. UPDATE statements that modify indexed columns and INSERT and DELETE statements that modify indexed tables take longer than if there were no index. Such SQL statements must modify data in indexes as well as data in tables.

`db_index = True`  e.g quereis frequent filter, order-by etc.


