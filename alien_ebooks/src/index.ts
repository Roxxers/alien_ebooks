import { SubredditMarkovEndpoint } from "./api_endpoints";
// tslint:disable-next-line: no-var-requires
require("./scss/bulma.scss");


const API_ROOT: string = "/api/v1";
const SUBREDDIT_ROOT: string = `${API_ROOT}/subreddits`;


function createBulmaElement(tag: string, classes: string): HTMLElement {
    const element = document.createElement(tag);
    element.classList.add(classes);
    return element;
}

function createMediaElement(): HTMLElement {
    const article = createBulmaElement("article", "media");
    const mediaContent = createBulmaElement("div", "media-content");
    const contentWrapper = createBulmaElement("div", "content");
    mediaContent.appendChild(contentWrapper);
    article.appendChild(mediaContent);
    return article;
}

function createTitleElements(titles: string[]): HTMLElement[] {
    const articles: HTMLElement[] = [];
    titles.forEach(title => {
        const article = createMediaElement();
        const contentElement = document.createElement("p");
        contentElement.innerHTML = `<strong>${title}</strong>`;
        article.children[0].children[0].appendChild(contentElement);
        articles.push(article);
    });
    return articles;
}

function add_titles_to_html(response: SubredditMarkovEndpoint): void {
    const data: string[] = response.data;
    const titles: HTMLElement = document.getElementById("gen");
    let title: HTMLParagraphElement;

    while (titles.firstChild) {
        titles.removeChild(titles.firstChild);
    }

    if (response.data == null) {
        title = document.createElement("p");
        title.innerHTML = "404";
        titles.appendChild(title);
        // TODO: Update this to make more sense
    } else {
        const posts = createTitleElements(data);
        posts.forEach(title => titles.appendChild(title));
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

