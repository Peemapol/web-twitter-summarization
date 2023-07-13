var time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit", hour12: false });
var date = new Date().toLocaleDateString();
var timeDate = time + " · " + date;
console.log(timeDate)
document.getElementById('bot-tweet-date').innerText = timeDate;