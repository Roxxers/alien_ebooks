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

import * as api from "./api/api";
import { MarkovPost, SubredditMarkovEndpoint, TaskData } from "./api/endpoints";
import { createTitleElements } from "./elements";
import { loadingBar, updateLoadingBar } from "./loadingBar";

import "../sass/bulma.scss";

import io from "socket.io-client";


const socket = io();
socket.on("connect", () => {
    socket.emit("my event", {data: "I'm connected!"});
    console.log("Connected");
});

socket.on("message", (message: string) => {
    console.log(message);
});

socket.on("build_update", async (task: TaskData) => {
    console.log(task);
    await updateLoadingBar(task);
});

/**
 * Add posts to the page.
 * Removes posts from previous requests if they exist.
 * @param response - API response object to use the posts from
 */
function add_titles_to_html(response: SubredditMarkovEndpoint): void {
    const data: MarkovPost[] = response.data;
    const titles: HTMLElement = document.getElementById("GeneratedPosts");

    while (titles.firstChild) {
        titles.removeChild(titles.firstChild);
    }

    if (response.response_code === 404) {

    } else {
        const posts = createTitleElements(data);
        posts.forEach(title => titles.appendChild(title));
        // TODO: Deal with null title objects
    }
}

async function requestSubredditCreation(subreddit: string): Promise<void> {
    return api.makeBuildRequest(subreddit)
        .then(taskID => {
            socket.emit("build_request", {buildID: taskID});
            console.log("Build request emitted for: ", taskID);
            loadingBar.classList.remove("is-hidden");
        });
}

/**
 * Listener function to make api request and add markov posts to the page
 * @param event - event this function is listening on
 */
async function titleRequestListener(event: Event): Promise<void> {
    event.preventDefault();
    const button = document.getElementById("SubredditSubmitButton") as HTMLButtonElement;
    button.disabled = true;
    const form: HTMLFormElement = document.forms.namedItem("sInput");
    const subreddit: string = form.sName.value;

    await api.checkSubredditExists(subreddit)
        .then(async exists => {
            if (!exists) {
                await requestSubredditCreation(subreddit);
            } else {
                const titles = await api.requestTitles(subreddit);
                add_titles_to_html(titles);
            }
        });
    button.disabled = false;
}

// Get subreddit form
const form: HTMLElement = document.getElementById("subreddit_request_form");
form.addEventListener("submit", titleRequestListener, true);
