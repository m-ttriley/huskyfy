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

var Buildings = mongoose.model('Building', 
    mongoose.Schema({
        _id: Number, 
        latitude: Number,
        display_name: String,
        types: [String],
        name: String,
        longitude: Number,
    }),
    'buildings');

var Songs = mongoose.model('Song',
    mongoose.Schema({
        building_id: Number,
        user: String,
        uri: String,
        title: String,
        album: String,
        artist: String
    }), 
    'songs');




/*
function getCollection(collec) {
    return mongoose.connection.db.collection(collec);
}
function find (collec, query, callback) {
    mongoose.connection.db.collection(collec, function (err, collection) {
    collection.find(query).toArray(callback);
    });
}
*/
function findClosestBuilding (lat, longitude, buildings) {
    // Math.abs(x1-x0) + Math.abs(y1-y0)
    var distance = 10000;
    var closestBuilding = null;
    buildings.map(function(building) {
        var currentDistance = Math.abs(lat - building.latitude) + Math.abs(longitude - building.longitude);
        if (currentDistance < distance) {
            distance = currentDistance;
            closestBuilding = building;
        }
    });

    return closestBuilding;
}


app.use(express['static'](__dirname + '/public'));
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ 'extended': 'true' }));
app.use(bodyParser.json()); // parse application/json
app.use(bodyParser.json({ type: 'application/vnd.api+json' })); // parse application/vnd.api+json as json
app.use(methodOverride('X-HTTP-Method-Override'));


app.get('/api/building/:latitude/:longitude', function (req, res, next) {
    Buildings.find(function(err, buildings) {
        var loc = findClosestBuilding(req.params.latitude, req.params.longitude, buildings);
        res.json(loc);
    });
});


app.get('/api/songs/:buildingID', function (req, res, next) {
    Songs.find({
        building_id: req.params.buildingID
    }, function(err, songs) {
        res.json(songs);
    });
});
// posting a new song to our database
app.post('/api/song', function (req, res) {
    console.log(req.body.building_id);
    console.log(req.body.uri);
    console.log(req.body.title);
    console.log(req.body.artist);
    console.log(req.body.album);
    console.log(req.body.user);
    console.log(req.body.date);
    console.log("post started");

    var newSong = new Song({
        building_id: req.body.building_id,
        uri: req.body.uri,
        title: req.body.title,
        artist: req.body.artist,
        album: req.body.album,
        user: req.body.user,
        date: req.body.date
    }).save(function(err) {
        console.log(err);
    });

    Songs.find({
        building_id: req.params.building
    }, function(err, songs) {
        res.json(songs);
    });
});


app.get('/', function (req, res) {
    res.sendfile('./public/index.html');
});

app.listen(9000);
console.log('app listening on 9000');
