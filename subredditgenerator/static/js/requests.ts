

const api_root: string = "/api/v1";
const subreddit_root: string = `${api_root}/subreddits`


function add_titles_to_html(data: JSON): void {
    var title: HTMLElement = document.getElementById('gen');

    if (data["data"] == null) {
        title.innerHTML = "404";
    } else {
        if (data["data"] == null) {
            title.innerHTML = "null";
        } else {
            title.innerHTML = data["data"][0];
        }
    }
}

function api_request() {
        let data: JSON = JSON.parse(this.response);
        add_titles_to_html(data);
}

// Wrapper function to prevent the default submit and run the get_titles function
function request_titles(event: Event): void {
    // We let button have any type here because otherwise the complier will complain that HTMLElement doesn't have 'disabled'
    let button: any = document.getElementById("SubredditSubmitButton");
    button.disabled = true;

    const subreddit: string = document.forms["sInput"]["sName"].value;
    const url: string = `${subreddit_root}/${subreddit}/markov?amount=1`
 
    var request = new XMLHttpRequest();

    request.onload = api_request;
    request.open('GET', url, true);
    request.send();

    button.disabled = false;

    event.preventDefault();
};

// Get subreddit form
var form : HTMLElement = document.getElementById("subreddit_request_form");

// attach event listener
form.addEventListener("submit", request_titles, true);

