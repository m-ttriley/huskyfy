'use strict';

var fs = require('fs');
var express = require('express');
var app = express();
var mongoose = require('mongoose');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var mongodb = require('mongodb');
var url = 'mongodb://matt:riley@ds053794.mongolab.com:53794/huskyfy';
var SpotifyWebApi = require('spotify-web-api-node');
var spotifyApi = new SpotifyWebApi();

var connect = function connect() {
    var options = { server: { socketOptions: { keepAlive: 1 } } };
    mongoose.connect(url, options);
};

connect();

mongoose.connection.on('error', console.log);
mongoose.connection.on('disconnected', connect);

function getCollection(collec, )
function find (collec, query, callback) {
    mongoose.connection.db.collection(collec, function (err, collection) {
    collection.find(query).toArray(callback);
    });
}

app.use(express['static'](__dirname + '/public'));
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ 'extended': 'true' }));
app.use(bodyParser.json()); // parse application/json
app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json
app.use(methodOverride('X-HTTP-Method-Override'));

/*
// return the URI of top search result for the given track name
function getSpotifyUri(songName) {
    spotifyApi.searchTracks(songName, {limit: 1})
    .then(function(data) {
        var uri = data.body.tracks.items[0].uri;
        console.log('Spotify URI of', songName, uri, "\n");
        updatePlayer(uri);
    }, function(err) {
        console.error(err);
    });
}
*/

// getSpotifyUri("Technologic");

// SCHEMA GOES HERE:
var Song = mongoose.model('Song', {
    building: Number,
    trackURL: String,
    artist: String,
    album: String,
    date: Date

});


// to get the whole list of songs
app.get('/api/song', function (req, res) {

    Song.find(function (err, users) {
        if (err) res.send(err);

        res.json(users);
    });
});


// posting a new song to our database
app.post('/api/song', function (req, res) {
    console.log(req.body.building);
    console.log(req.body.trackURL);
    console.log(req.body.artist);
    console.log(req.body.album);
    console.log(req.body.date);
    console.log("post started");

    var newSong = new Song({
        building: req.body.building,
        trackURL: req.body.trackURL,
        artist: req.body.artist,
        album: req.body.album,
        date: req.body.date
    });

    newSong.save(function (err) {
        if (err) console.log('registration failed');
    });

    Song.find(function (err, users) {
        if (err) res.send(err);

        console.log(users);
    });
});

app.get('/', function (req, res) {
    res.sendfile('./public/index.html');
});

app.listen(9000);
console.log('app listening on 9000');
