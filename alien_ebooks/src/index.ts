// alien_ebooks
// Copyright (C) 2019  Roxanne Gibson

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

import { MarkovPost, SubredditMarkovEndpoint } from "./endpoints";
// tslint:disable-next-line: no-var-requires
require("./scss/bulma.scss");


const API_ROOT: string = "/api/v1";
const SUBREDDIT_ROOT: string = `${API_ROOT}/subreddits`;


function createBulmaElement(tag: string, classes: string): HTMLElement {
    const element = document.createElement(tag);
    const classList = classes.split(" ");
    classList.forEach(cssClass => {
        element.classList.add(cssClass);
    });
    return element;
}

function createMediaElement(): HTMLElement {
    // Base Element
    const article = createBulmaElement("article", "media");
    // Media-left, image placeholder
    const mediaImage = createBulmaElement("div", "media-left");
    const image = createBulmaElement("img", "image is-64x64") as HTMLImageElement;
    image.src = "https://bulma.io/images/placeholders/128x128.png";
    mediaImage.appendChild(image);
    // Media Content
    const mediaContent = createBulmaElement("div", "media-content");
    const contentWrapper = createBulmaElement("div", "content");
    mediaContent.appendChild(contentWrapper);
    // Add all elements to base element
    article.appendChild(mediaImage);
    article.appendChild(mediaContent);
    return article;
}

function createTitleElements(posts: MarkovPost[]): HTMLElement[] {
    const articles: HTMLElement[] = [];
    posts.forEach(post => {
        const article = createMediaElement();
        const contentElement = document.createElement("p");

        let title = `<strong>${post.title}</strong>`;
        if (post.nsfw) {
            title += ` <span class="nsfw">NSFW</span>`;
        }

        const postMetaLine = `<span class="has-text-grey is-size-7"><strong>r/${post.subreddit}</strong> by u/exampleuser`;
        const commentsCounter = `<i class="fas fa-comment-alt"></i> ${post.comments} Comments</span>`;


        contentElement.innerHTML = `${title}<br>${postMetaLine}<br>${commentsCounter}`;
        const mediaContent = article.getElementsByClassName("media-content");
        mediaContent[0].children[0].appendChild(contentElement);
        articles.push(article);
    });
    return articles;
}

function add_titles_to_html(response: SubredditMarkovEndpoint): void {
    const data: MarkovPost[] = response.data;
    const titles: HTMLElement = document.getElementById("GeneratedPosts");
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
        // TODO: Deal with null title objects
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

