var Container = React.createClass({
    getInitialState: function() {
        return {currentSong: 'https://embed.spotify.com/?uri=spotify%3Atrack%3A33Q6ldVXuJyQmqs8BmAa0k'};
    },

    songA: function() {
        this.setState({
            currentSong: 'https://embed.spotify.com/?uri=spotify%3Atrack%3A33Q6ldVXuJyQmqs8BmAa0k'
        });
    },

    songB: function() {
        this.setState({
            currentSong: 'https://embed.spotify.com/?uri=spotify%3Atrack%3A5H25xsIuRWUI8GwcoAoeSG' 
        });
    },

    render: function() {
        return (
            <div>
            <div> 
            <button type='button' onClick={this.songA} />
            <Player song={this.state.currentSong} />
            <button type='button' onClick={this.songB} />
            </div>
            <div>
            <Signup url="/api/song" />
            </div>
            </div>
            );
        }
    });

var Player = React.createClass({
    render: function() {
        return (
            <iframe src={this.props.song} width="300" height="380" frameborder="0" allowtransparency="true"></iframe>
            );
    }
});

var Signup = React.createClass({

    handleSignup: function(data) {
      $.ajax({
        url: this.props.url,
        dataType: 'json',
        type: 'POST',
        data: data,
        success: function(data) {
          console.log(data);
        },
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    },

    render: function() {
      return (
        <div>
          <SignupForm handleSignup={this.handleSignup} />
        </div>
      );
    }
  });

  var SignupForm = React.createClass({
    handleSubmit: function(e) {
    e.preventDefault();
    var building = React.findDOMNode(this.refs.building).value.trim();
        var trackURL = React.findDOMNode(this.refs.trackURL).value.trim();
        if (!trackURL || !building) {
            return;
          }
        this.props.handleSignup({
          building: building,
          trackURL: trackURL
        });
        React.findDOMNode(this.refs.building).value = '';
        React.findDOMNode(this.refs.trackURL).value = '';
        return;
      },

      render: function() {
        return (
          <form className="signupForm" onSubmit={this.handleSubmit}>
            <input type="number" placeholder="enter the building ID" ref="building" />
            <input type="text" placeholder="enter the song URL" ref="trackURL" />
            <input type="submit" value="sign up" />
          </form>
          );
      }
  });

ReactDOM.render(
    <Container />, 
    document.getElementById('content'));