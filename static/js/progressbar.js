const socket = io("https://twitter-summarization-96cc58b75ed0.herokuapp.com/");
let socketid = undefined;
// socket.connect("https://twitter-summarization-96cc58b75ed0.herokuapp.com/");
socket.on("connect", function(){
    socketid = socket.id;
    console.log('connected');
    console.log(socketid);
})

let progress_container = document.getElementById("progressbar-container");
let progress = document.getElementById("main-progressbar");
let information = document.getElementById("basic-info");
let goBtn = document.getElementById('submit-main-form');

socket.on("update progress", function(percent){
    progress_container.style.display = "block";
    console.log("Got percent: " + percent);
    progress.style.width = percent + "%";
    if(percent == 100){
        document.getElementById("progress-text").classList.remove("animate-flicker");
    }
})

let mainForm = document.getElementById("main-form");
mainForm.addEventListener('submit', event => {
    console.log("catch onsubmit");
    alert('this function is disabled right not!')
    return
    event.preventDefault();
    goBtn.style.backgroundColor = 'var(--light-gray-twitter)';
    goBtn.disabled = true;
    
    const formData = new FormData(mainForm);

    const hashtag = formData.get('hashtag');
    const n_tweets = formData.get('number_of_tweets');
    const tweet_date_early = formData.get('tweet_date_early');
    const tweet_date_later = formData.get('tweet_date_later');
    const snscrape = formData.get('snscrape');
    const selenium = formData.get('selenium');
    
    document.getElementById('input-hashtag-is').innerText = 'Your input is ' + hashtag;

    document.getElementById("progress-text").classList.add("animate-flicker");

    socket.emit('formSubmit', { hashtag: hashtag, n_tweets: n_tweets, tweet_date_early: tweet_date_early, 
        tweet_date_later: tweet_date_later, snscrape: snscrape, selenium: selenium ,socketid: socketid });
});

socket.on('createTable', data => {
    const tableBody = document.getElementById('tweet-table');
    tableBody.innerHTML = '';

    data.tweetList.forEach(tweet => {
        const newRow = document.createElement('tr');
        const tweetCell = document.createElement('td');

        tweetCell.textContent = tweet;
        newRow.appendChild(tweetCell);
        tableBody.appendChild(newRow);
    })
})

socket.on('createEmbeded', data => {
    const gridBody = document.getElementById('embeded-container');
    gridBody.innerHTML = '';
    var i = 0;
    var retweetList = data.reTweetCount;
    var likeList = data.likeCount;
    data.embededHtml.forEach(tweet => {
        var new_item = document.createElement('div');
        new_item.className = "twitter-tweet";
        var showRetweet = document.createElement('div');
        showRetweet.className = "twitter-retweet-container";
        var retweetCount = document.createElement('p');
        retweetCount.className = "retweet-number";
        retweetCount.setAttribute("data-target", retweetList[i])
        var retweetText = document.createElement('p');
        retweetText.className = "reTweetText";
        var likesCount = document.createElement('p');
        likesCount.className = "retweet-number";
        likesCount.setAttribute("data-target", likeList[i])
        var likesText = document.createElement('p');
        likesText.className = "reTweetText";
        new_item.innerHTML = tweet;
        retweetCount.innerText = '0';
        retweetText.innerText = "retweets";
        likesCount.innerText = '0';
        likesText.innerText = "likes";
        showRetweet.appendChild(retweetCount);
        showRetweet.appendChild(retweetText);
        showRetweet.appendChild(likesCount);
        showRetweet.appendChild(likesText);
        gridBody.appendChild(showRetweet);
        gridBody.appendChild(new_item);
        i += 1
    })
    var url = 'https://platform.twitter.com/widgets.js';
    $.getScript(url);
    $.getScript('static\\js\\countUp.js');
    $.getScript('static\\js\\dateTime.js');
    information.style.display = "block";
    goBtn.disabled = false;
    document.getElementById('quick-search-container').style.pointerEvents = 'auto';
    goBtn.style.backgroundColor = 'var(--blue-twitter)';
})

socket.on('taskName', function(task){
    const progressName = document.getElementById('progress-text');
    progressName.innerText = task;
})

$(document).ready(function() {
    $('p.news-hashtags').click(function() {
        document.getElementById('quick-search-container').style.pointerEvents = 'none';
        goBtn.style.backgroundColor = 'var(--light-gray-twitter)';
        goBtn.disabled = true;
        const hashtag = $(this).text();
        document.getElementById('input-hashtag-is').innerText = 'Quick search hashtag is ' + hashtag;
        document.getElementById("progress-text").classList.add("animate-flicker");
        $("html, body").animate({ scrollTop: 0 }, "slow");
        socket.emit('quickSearch', { hashtag: hashtag, socketid: socketid });
    });
});