var twitter = require("twit"),
    credentials = require("./credentials.js"),
    express = require("express"),
    app = express(),
    server = require("http").createServer(app),
    io = require("socket.io").listen(server);

var t = new twitter({
  consumer_key: credentials.consumer_key,
  consumer_secret: credentials.consumer_secret,
  access_token: credentials.access_token_key,
  access_token_secret: credentials.access_token_secret
});

app.get("/", function (req, res) {
  res.sendFile(__dirname + "/index.html");
});

server.listen(5000);

io.sockets.on("connection", function (socket) {
  // console.log("SOCKET CONNECTED\n");
  var track_item = ["#food", "#photography", "#pets", "#funny",
                    "#happybirthday", "#movies", "#foodporn",
                    "#friends", "#bitcoin", "#ico"];
  var twitterStream = t.stream(
      "statuses/filter",
      { track: track_item }
  );

  twitterStream.on("tweet", function (tweet) {
    matchedHashtag = containsAny(tweet.text, track_item)
    if (tweet && matchedHashtag) {
      // console.log(tweet.text)
      io.sockets.emit("stream", {detail: tweet, hashtag: matchedHashtag});
    }
  });

  twitterStream.on("error", function (error) {
    throw error;
  });
});

function containsAny(str, substrings) {
  for (var i = 0; i != substrings.length; i++) {
    var substring = substrings[i];
    if (str.indexOf(substring) != -1) {
      return substring;
    }
  }
  return null;
}
