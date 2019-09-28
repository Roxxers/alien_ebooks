

function get_titles(amount: number) {
    
    const subreddit: string = document.forms["sInput"]["sName"].value;
    const url: string = "/api/v1/subreddits/" + subreddit + "/markov?amount=" + amount;

    var request = new XMLHttpRequest();

    request.onload = function() {
        var data: JSON = JSON.parse(this.response);
        var title: HTMLElement = document.getElementById('gen');

        title.innerHTML = data["data"];
    }
    
    request.open('GET', url, true);
    request.send();
}


// Wrapper function to prevent the default submit and run the get_titles function
function request_titles(event: Event) {
    // We let button have any type here because otherwise the complier will complain that HTMLElement doesn't have 'disabled'
    let button: any = document.getElementById("SubredditSubmitButton");
    button.disabled = true;
    get_titles(1);
    button.disabled = false;

    event.preventDefault();
};

// Get subreddit form
var form : HTMLElement = document.getElementById("subreddit_request_form");

// attach event listener
form.addEventListener("submit", request_titles, true);

