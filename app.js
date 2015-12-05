

    var Container = React.createClass({
    getInitialState: function() {
        return {currentSong: 'https://embed.spotify.com/?uri=spotify%3Atrack%3A33Q6ldVXuJyQmqs8BmAa0k'}
    },

    songA: function() {
        this.setState({
            currentSong: 'https://embed.spotify.com/?uri=spotify:user:121023616:playlist:0hmTkcOW36gH3JA53ILYZE'
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

    handleSearch: function(query) {
      $.ajax({
        url: 'https://api.spotify.com/v1/search',
        type: 'GET',
        data: {
          q: query,
          type: 'track'
        },
        success: function(data) {
          // todo: add this to the database
          console.log(data.tracks.items[0].uri);
        },
        error: function(xhr, status, err) {
          console.error(this.props.url, status, err.toString());
        }.bind(this)
      });
    },

    render: function() {
      return (
        <div>
          <SignupForm handleSearch={this.handleSearch} />
        </div>
      );
    }
  });

  var SignupForm = React.createClass({
    handleSubmit: function(e) {
    e.preventDefault();
        var trackURL = React.findDOMNode(this.refs.trackSearch).value.trim();
        if (!trackURL) {
            return;
          }
        this.props.handleSearch(trackURL);
        ReactDOM.findDOMNode(this.refs.trackSearch).value = '';
        return;
      },

      render: function() {
        return (
          <form className="signupForm" onSubmit={this.handleSubmit}>
            <input type="text" placeholder="Search for a song to add" ref="trackSearch" />
            <input type="submit" value="Add a song" />
          </form>
          );
      }
  });

ReactDOM.render(
    <Container />, 
    document.getElementById('content'));