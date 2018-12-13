https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends-legacy

![](../images/followers1.png)

The following query returns the process_id value from the process table and then some values from multiple records from the table obj_property - if those records exist - correlated via an intermediate table route. Complex, but also fast!

    SELECT process.process_id, op1.value_int, op2.value_string, op3.value_string
    FROM process
      INNER JOIN route ON ( route.route_id = process.route_id )
      LEFT OUTER JOIN obj_property op1
        ON ( op1.obj_id = route.route_id AND
             op1.namespace_prefix = 'http://www.opengroupware.us/oie' AND
             op1.value_key = 'expireDays' )
      LEFT OUTER JOIN obj_property op2
        ON ( op2.obj_id = route.route_id AND
             op2.namespace_prefix = 'http://www.opengroupware.us/oie' AND
             op2.value_key = 'preserveAfterCompletion' )
      LEFT OUTER JOIN obj_property op3
        ON ( op3.obj_id = route.route_id AND
             op3.namespace_prefix = 'http://www.opengroupware.us/oie' AND
             op3.value_key = 'archiveAfterExpiration' )
    WHERE process.db_status != 'archived'
      AND process.state IN ( 'C', 'F', 'Z' )
      AND process.status != 'archived';

The SQLAlchemy `aliased()` method declares multiple references to `ObjectProperty` that can be used independently: `op1`, `op2`, and `op3`. The other advanced technique is to use the `outerjoin()` method to relate the need for a LEFT OUTER join.

    op1 = aliased(ObjectProperty)
    op2 = aliased(ObjectProperty)
    op3 = aliased(ObjectProperty)

    q = Session.query( Process, op1, op2, op3 ).\
           join( Route, Route.object_id == Process.route_id ).\
           outerjoin( op1, and_( op1.parent_id == Route.object_id,
                                 op1.namespace=='http://www.opengroupware.us/oie',
                                 op1.name=='expireDays' ), ).\
           outerjoin( op2, and_( op2.parent_id == Route.object_id,
                                 op2.namespace=='http://www.opengroupware.us/oie',
                                 op2.name=='preserveAfterCompletion' ), ).\
           outerjoin( op3, and_( op3.parent_id == Route.object_id,
                                 op3.namespace=='http://www.opengroupware.us/oie',
                                 op3.name=='archiveAfterExpiration' ), ).\
           filter( and_( Process.state.in_( [ 'C', 'F', 'Z' ] ),
                         Process.status != 'archived' ) )

The results of this query will be tuples of four elements; the first being a Process object and the second, third, and fourth will either be ObjectProperty objects if the concomitant outer join identified a record or None if no record matched the join. The lovely upside of this is that the query results can be processed using a straight forward for-each construct:

    for process, expire_days, preserve_after, archive_after in q.all():
       if expire_days:
           ....




