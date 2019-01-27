Transactions are a fundamental concept of all database systems. Atomicity is the defining property of database transactions. The essential point of a transaction is that it bundles multiple steps into a single, all-or-nothing operation. The intermediate states between the steps are not visible to other concurrent transactions, and if some failure occurs that prevents the transaction from completing, then none of the steps affect the database at all.

Consider a simplified example of a bank database where we want to transfer money from one persons account to anothers, the SQL commands for this might look like:

    UPDATE accounts SET balance = balance - 100.00
        WHERE name = 'Alice';
    UPDATE branches SET balance = balance - 100.00
        WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Alice');
    UPDATE accounts SET balance = balance + 100.00
        WHERE name = 'Bob';
    UPDATE branches SET balance = balance + 100.00
        WHERE name = (SELECT branch_name FROM accounts WHERE name = 'Bob');

The details of these commands are not important here; the important point is that there are several separate updates involved to accomplish this rather simple operation.
It would certainly not do for a system failure to result in Bob receiving $100.00 that was not debited from Alice etc.
We need a guarantee that if something goes wrong partway through the operation, none of the steps executed so far will take effect.
Grouping the updates into a transaction gives us this guarantee. A transaction is said to be atomic: from the point of view of other transactions, it either happens completely or not at all.

Another important property of transactional databases is closely related to the notion of atomic updates: when multiple transactions are running concurrently, each one should not be able to see the incomplete changes made by others. For example, if one transaction is busy totalling all the branch balances, it would not do for it to include the debit from Alice's branch but not the credit to Bob's branch, nor vice versa. So transactions must be all-or-nothing not only in terms of their permanent effect on the database, but also in terms of their visibility as they happen. The updates made so far by an open transaction are invisible to other transactions until the transaction completes, whereupon all the updates become visible simultaneously.

In PostgreSQL, a transaction is set up by surrounding the SQL commands of the transaction with BEGIN and COMMIT commands. So our banking transaction would actually look like:

    BEGIN;
    UPDATE accounts SET balance = balance - 100.00
        WHERE name = 'Alice';
    -- etc etc
    COMMIT;

If, partway through the transaction, we decide we do not want to commit (perhaps we just noticed that Alice's balance went negative), we can issue the command ROLLBACK instead of COMMIT, and all our updates so far will be canceled.
PostgreSQL actually treats every SQL statement as being executed within a transaction. If you do not issue a BEGIN command, then each individual statement has an implicit BEGIN and (if successful) COMMIT wrapped around it. A group of statements surrounded by BEGIN and COMMIT is sometimes called a transaction block.

*Note that transactions do not inherently prevent all race conditions. In practice, you still need locking, abort-and-retry handling, or other protective measures in all real-world database implementations*









