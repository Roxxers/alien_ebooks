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

/**
 * Creates element that fits with the bulma framework
 * @param tag - html tag for element
 * @param classes - list of space separated classes to add to the element
 * @returns Bulma HTML Element
 */
function createBulmaElement(tag: string, classes: string): HTMLElement {
    const element = document.createElement(tag);
    const classList = classes.split(" ");
    classList.forEach(cssClass => {
        element.classList.add(cssClass);
    });
    return element;
}

/**
 * Creates a Bulma Media element.
 * This is used for generated posts.
 * @returns Bulma Media element
 */
function createMediaElement(): HTMLElement {
    // Base Element
    const article = createBulmaElement("article", "media");
    // Media-left, image placeholder
    const mediaImage = createBulmaElement("div", "media-left");
    const image = createBulmaElement("div", "placeholder");
    image.innerHTML = `<i class="fas fa-quote-left placeholder-icon"></i>`;
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

/**
 * Creates post elements from api results
 * @param posts - markov posts from the api
 * @returns list of media objects
 */
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


/**
 * Add posts to the page.
 * Removes posts from previous requests if they exist.
 * @param response - API response object to use the posts from
 */
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

/**
 * Listener function to make api request and add markov posts to the page
 * @param event - event this function is listening on
 */
function request_titles(event: Event): void {
    const button = document.getElementById("SubredditSubmitButton") as HTMLButtonElement;
    button.disabled = true;

    const form: HTMLFormElement = document.forms.namedItem("sInput");
    const subreddit: string = form.sName.value;
    const url: string = `${SUBREDDIT_ROOT}/${subreddit}/markov?amount=5`;

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
form.addEventListener("submit", request_titles, true);
