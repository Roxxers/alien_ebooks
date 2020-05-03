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

import { createTitleElements } from "./elements";
import { MarkovPost, SubredditBuildRequest, SubredditMarkovEndpoint, TaskData } from "./endpoints";

import "../sass/bulma.scss";

import io from "socket.io-client";


const API_ROOT: string = "/api/v1";
const SUBREDDIT_ROOT: string = `${API_ROOT}/subreddits`;

const loadingBarContainer: HTMLElement = document.getElementById("LoadingBar");
const bar = document.createElement("div");
loadingBarContainer.appendChild(bar);


const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
};

var socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    console.log("Connected");
});

socket.on("message", function(message) {
    console.log(message);
});

socket.on("build_update", async (task: TaskData) => {
    console.log(task);
    if (task.state === "FINISHED") {
        bar.innerHTML = "";
        // Do something before delay
        await sleep(5500);
        await requestTitles(task.subreddit);
        // Do something after
    } else {
        let percent: number;
        percent = (task.current / task.total) * 100;
        percent = Math.round(percent);
        console.log("Percent complete: ", percent);
        bar.innerHTML = `<progress id="downloading_percentage" class="progress is-primary" value="${percent}" max="100">${percent}%</progress>`;
    }
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


async function requestTitles(subreddit: string): Promise<void> {
    const url: string = `${SUBREDDIT_ROOT}/${subreddit}/markov?amount=5`;
    await fetch(url)
        .then(async res => {
            add_titles_to_html(await res.json() as SubredditMarkovEndpoint);
        });
}

async function requestSubredditCreation(subreddit: string): Promise<void> {
    return makeBuildRequest(subreddit)
        .then(taskID => {
            bar.innerHTML = `<progress id="downloading_percentage" class="progress is-primary" value="0" max="100">0%</progress>`;
            socket.emit("build_request", {buildID: taskID});
            console.log("Build request emitted for: ", taskID);
        });

}

async function makeBuildRequest(subreddit: string): Promise<string> {
    const url = `${API_ROOT}/subreddits/${subreddit}`;
    const data = await fetch(url, {method: "POST"});
    const res = await (data.json() as Promise<SubredditBuildRequest>);
    return res.data.task_id;
}


async function checkSubredditExists(subreddit: string): Promise<boolean> {
    const url: string = `${SUBREDDIT_ROOT}/${subreddit}`;
    return fetch(url)
        .then(res => {
            if (res.status === 200) {
                return true;
            } else if (res.status === 404) {
                return false;
            } else {
                return null; // If this happens something has seriously gone wrong
            }
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

    await checkSubredditExists(subreddit)
        .then(async exists => {
            if (!exists && exists != null) {
                await requestSubredditCreation(subreddit);
            } else if (exists === null) {
                console.error("Shit fucked yo");
            }
            await requestTitles(subreddit);
        }
    );
    button.disabled = false;
}

// Get subreddit form
const form: HTMLElement = document.getElementById("subreddit_request_form");
form.addEventListener("submit", titleRequestListener, true);
