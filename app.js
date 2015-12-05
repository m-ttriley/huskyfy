var Container = React.createClass({
    getInitialState: function() {
        return {currentSong: 'https://embed.spotify.com/?uri=spotify%3Atrack%3A33Q6ldVXuJyQmqs8BmAa0k',
                loc: {this.getLocation()};
    },

    getLocation: function() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
        var latlon = position.coords.latitude + "," + position.coords.longitude;

        var img_url = "http://maps.googleapis.com/maps/api/staticmap?center="+latlon+"&zoom=14&size=400x300&sensor=false";

        return img_url;

    } else {
        console.log("Geolocation is not supported by this browser.");
    }
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

    setSong: function(uri) {
      this.setState({
            currentSong:  'https://embed.spotify.com/?uri=' + uri;
      })
    },

    render: function() {
        return (
            <div>
            <div>
            <img src={this.state.loc} />
            </div>
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
            <iframe src={this.props.song} width="300" height="380" frameBorder="0" allowTransparency="true"></iframe>
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