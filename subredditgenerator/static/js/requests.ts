

function get_titles(amount:number) {
    var request = new XMLHttpRequest()
    var subreddit: string = document.forms["sInput"]["sName"].value

    var url: string = "/api/v1/subreddit/" + subreddit + "/markov?amount=1"

    request.open('GET', url, true)
    
    request.onload = function() {
        var title = document.getElementById('gen')
        var data = JSON.parse(this.response)
        title.innerHTML = data
    }
    
    request.send()
}


// Wrapper function to prevent the default submit and run the get_titles function
var request_titles = function(event) {
    get_titles(1);
    event.preventDefault();
};

// Get subreddit form
var form = document.getElementById("subreddit_request_form");

// attach event listener
form.addEventListener("submit", request_titles, true);