import { SubredditMarkovEndpoint } from "./api_endpoints";
require("./scss/bulma.scss");


const API_ROOT: string = "/api/v1";
const SUBREDDIT_ROOT: string = `${API_ROOT}/subreddits`;


function add_titles_to_html(response: SubredditMarkovEndpoint): void {
    const data: string[] = response.data;
    const titleDiv: HTMLElement = document.getElementById("gen");
    let title: HTMLParagraphElement;

    while (titleDiv.firstChild) {
        titleDiv.removeChild(titleDiv.firstChild);
    }

    if (response.data == null) {
        title = document.createElement("p");
        title.innerHTML = "404";
        titleDiv.appendChild(title);
    } else {
        for (let i = 0; i < data.length; i++) {
            title = document.createElement("p");
            if (data[i] == null) {
                title.innerHTML = "null";
            } else {
                title.innerHTML = data[i];
            }
            titleDiv.appendChild(title);
        }
    }
}

// Wrapper function to prevent the default submit and run the get_titles function
function request_titles(event: Event): void {
    const button = document.getElementById("SubredditSubmitButton") as HTMLButtonElement;
    button.disabled = true;

    const form: HTMLFormElement = document.forms.namedItem("sInput");
    const subreddit: string = form.sName.value;
    const url: string = `${SUBREDDIT_ROOT}/${subreddit}/markov?amount=10`;

    const request = new XMLHttpRequest();

    request.onload = function(): void {
        const response: SubredditMarkovEndpoint = JSON.parse(this.response);
        add_titles_to_html(response);
    };
    request.open("GET", url, true);
    request.send();

    button.disabled = false;

    event.preventDefault();
}

// Get subreddit form
const form: HTMLElement = document.getElementById("subreddit_request_form");

// attach event listener
form.addEventListener("submit", request_titles, true);

