Pass functions to attributes like `onChange`:

    class MyComponent extends Component {
      render () {
        <input type="text"
            value={this.state.value}
            onChange={event => this.onChange(event)} />
      }

      onChange (event) {
        this.setState({ value: event.target.value })
      }
    }



