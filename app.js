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
            <button type='button' onClick={this.songA} />
            <Player song={this.state.currentSong} />
            <button type='button' onClick={this.songB} />
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

var CommentBox = React.createClass({
  render: function() {
    return (
      <div className="commentBox">
        Hello, world! I am a CommentBox.
      </div>
    );
  }
});

ReactDOM.render(
    <Container />, 
    document.getElementById('content'));