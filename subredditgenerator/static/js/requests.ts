

function get_titles(amount: number) {
    var request = new XMLHttpRequest();
    var subreddit: string = document.forms["sInput"]["sName"].value;

    var url: string = "/api/v1/subreddits/" + subreddit + "/markov?amount=" + amount;

    request.open('GET', url, true);
    
    request.onload = function() {
        var title = document.getElementById('gen');
        var data = JSON.parse(this.response);

        title.innerHTML = data["data"];
    }
    
    request.send();
}


// Wrapper function to prevent the default submit and run the get_titles function
function request_titles(event: Event) {
    // We let button have any type here because otherwise the complier will complain that HTMLElement doesn't have atr 'disabled'
    let button: any = document.getElementById("SubredditSubmitButton");
    button.disabled = true;
    get_titles(1);
    button.disabled = false;
    event.preventDefault();
};

// Get subreddit form
var form = document.getElementById("subreddit_request_form");

// attach event listener
form.addEventListener("submit", request_titles, true);