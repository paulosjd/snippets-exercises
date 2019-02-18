**Two-way Binding**

![](../images/two-way-binding.png)

    var Tags = React.createClass({
      getInitialState: function(){
        return {
          selected:''
        }
      },
      setFilter: function(filter) {
        this.setState({selected  : filter})
        this.props.onChangeFilter(filter);
      },
      isActive:function(value){
        return 'btn '+((value===this.state.selected) ?'active':'default');
      },
      render: function() {
        return <div className="tags">
          <button className={this.isActive('')} onClick={this.setFilter.bind(this, '')}>All</button>
          <button className={this.isActive('male')} onClick={this.setFilter.bind(this, 'male')}>male</button>
          <button className={this.isActive('female')} onClick={this.setFilter.bind(this, 'female')}>female</button>
          <button className={this.isActive('child')} onClick={this.setFilter.bind(this, 'child')}>child</button>
          <button className={this.isActive('blonde')} onClick={this.setFilter.bind(this, 'blonde')}>blonde</button>
         </div>
      }
    });

**Curried function example**

    handleChange = field => e => {
          e.preventDefault()
          /// Do something here
        }

We'll start by representing it without using arrow functions …

    handleChange = function(field) {
      return function(e) {
        e.preventDefault()
        // Do something here
        // return ...
      };
    };

However, because arrow functions lexically bind this, it would actually look more like this …

    handleChange = function(field) {
      return function(e) {
        e.preventDefault()
        // Do something here
        // return ...
      }.bind(this)
    }.bind(this)

Maybe now we can see what this is doing more clearly. The `handleChange` function is creating a
function for a specified field. This is a handy React technique because you're required to setup
your own listeners on each input in order to update your applications state.
By using the `handleChange` function, we can eliminate all the duplicated code that would result
in setting up change listeners for each field.



