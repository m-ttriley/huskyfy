$(function() {
(function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        
    }
})();

function showPosition(position) {
    var latlon = position.coords.latitude + "," + position.coords.longitude;
    var img_url = "http://maps.googleapis.com/maps/api/staticmap?center=42.3380307,-71.0899268&zoom=17.33&size=500x660&sensor=false&markers=size:small%7Ccolor:0xff2600%7Clabel:2%7C" + latlon;

var Container = React.createClass({
    getInitialState: function() {
      return {
        building: '',
        songURL: ''
      };
    },

    componentDidMount: function() {
      $.get('/api/building/' + position.coords.latitude + '/' + position.coords.longitude, function(result) {
        if(this.isMounted()) {
        this.setState({
          building: result,
          songURL: '/api/songs/' + result._id
        });
      }
      }.bind(this));
    },

    render: function() {
        return (
            <div>
            <div id='title'>
                <span id="title"> huskyfy </span>
                <span id="subtitle"> {this.state.building.name} </span>
            </div>
              <div id='mapholder'>
                <img src={img_url} />
              </div>
              <div id='content'> 
                <Player building={this.state.building} url={this.state.songURL} />
              <div>
              </div>
              </div>
            </div>
            );
        },
    });

var Player = React.createClass({

  getInitialState: function() { 
    return {
      songs: ''
    };
  },

  componentWillReceiveProps: function(nextProps) { 
    $.get(nextProps.url, function(result) {
      if(result.length === 0) {

      }
      else {
      this.setState({
        songs: 'https://embed.spotify.com/?uri=spotify:trackset:' + nextProps.building.name + ':' + result.map(function(song) {
          return song.uri;
        }).reduce(function(previousValue, currentValue, currentIndex, array) {
          return previousValue + ',' + currentValue;
        })
      });
    }
    }.bind(this));

  },

  updateSongs: function() {
    $.get(this.props.url, function(result) {
      console.log(result);
      this.setState({
        songs: 'https://embed.spotify.com/?uri=spotify:trackset:' + this.props.building.name + ':' + result.map(function(song) {
          return song.uri;
        }).reduce(function(previousValue, currentValue, currentIndex, array) {
          return previousValue + ',' + currentValue;
        })
      });
    }.bind(this));
  },

    render: function() {
        return (
            <div>
            <iframe src={this.state.songs} width="500" height="500" frameBorder="0" allowTransparency="true"></iframe>
            <Signup updateSongs={this.updateSongs} building={this.props.building._id} />
            </div>
        );
    }
    });

var Signup = React.createClass({
  getInitialState: function() {
    return {};
  },

  handleSearch: function(query, username) {
    var self = this;
    console.log(username);
      $.ajax({
        url: 'https://api.spotify.com/v1/search',
        type: 'GET',
        data: {
          q: query,
          type: 'track'
        },
        success: function(data) {
          console.log(data);
          $.ajax({
            url: '/api/songs/',
            type: 'POST',
            data: {
              track: data.tracks.items[0],
              building: self.props.building,
              user: username
            },
            success: function(data) {
              self.props.updateSongs();
            },
            error: function(xhr, status, err) {
            console.error(status, err.toString());
            },
          });
        },
        error: function(xhr, status, err) {
          console.error(status, err.toString());
        }.bind(this)
      });
    },

    render: function() {
      return (
        <div>
          <SignupForm building={this.props.building} handleSearch={this.handleSearch} />
        </div>
      );
    }
  });

  var SignupForm = React.createClass({
    handleSubmit: function(e) {
    e.preventDefault();
        var trackURL = ReactDOM.findDOMNode(this.refs.trackSearch).value.trim();
        var username = ReactDOM.findDOMNode(this.refs.username).value.trim();
        if (!trackURL) {
            return;
          }
        if (!username) {
          username = "webuser";
        }
        this.props.handleSearch(trackURL, username);
        ReactDOM.findDOMNode(this.refs.trackSearch).value = '';
        ReactDOM.findDOMNode(this.refs.username).value = '';
        return;
      },

      render: function() {
        return (
          <form className="signupForm" onSubmit={this.handleSubmit}>
            <input type="text" placeholder="Search for a song to add" ref="trackSearch" />
            <input type="text" placeholder="Enter your name (optional)" ref="username" />
            <br /><input type="submit" value="Add a song" class="btn" />
          </form>
          );
      }
  });

ReactDOM.render(
    <Container />, 
    document.getElementById('main'));
};
function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            x.innerHTML = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "An unknown error occurred."
            break;
    }
}
});

