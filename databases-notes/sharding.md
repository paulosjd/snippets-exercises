Database sharding
-------------------
A highly scalable approach for improving the throughput and overall performance of high-transaction, large, database-centric business applications. It can be simply defined as a "shared-nothing" partitioning scheme for large databases across a number of servers, enabling new levels of database performance and scalability.  If you think of broken glass, you can get the concept of sharding-breaking your database down into smaller chunks called "shards" and spreading them across a number of distributed servers.

Each "shard" (running on its own server) contains a portion of the original monolithic database, and is "sharded" based on application-specific rules.  For example, many organizations "shard" by customer, with each shard containing a specific group of customer-related information.

The scalability of sharding is apparent and achieved through the distribution of processing across multiple shards and servers in the network. By hosting each shard database on its own server, the ratio between memory and data on disk is properly balanced, thereby reducing disk I/O and maximizing system resources. Databases rely heavily on the primary three components of any computer:  CPU, memory and disk. Each of these elements on a single server can only scale to a given point-after that, you need to take additional measures to improve performance. Disk I/O is the primary bottleneck, you cannot add an unlimited number of CPUs (or processing cores) and see a commensurate increase in performance without also improving the memory capacity and performance of the disk-drive subsystem.  

Sharding into smaller database allows for better managability. This is since production databases must undergo regular backups, optimization and other tasks. Routine table and index optimizations can stretch from hours to days, in some cases making regular maintenance infeasible. By using the sharding approach, each individual "shard" can be maintained independently, providing a far more manageable scenario.

**Considerations**

Sharding adds additional programming and operational complexity to your application. You lose the convenience of accessing the applications data in a single location. Managing multiple servers adds operational challenges. Before you begin, see whether sharding can be avoided or deferred. In implementing a sharding strategy, considerations include:

How the data is read? Databases are used to store and retrieve data. If we dont need to read data at all, we can simply write it to /dev/null. Data retrieval requirements heavily influence the sharding strategy.

How the data is distributed? Once you have a cluster of machines acting together, it is important to ensure that data and work is evenly distributed. Uneven load causes storage and performance hotspots. Some databases redistribute data dynamically, while others expect clients to evenly distribute and access data.


