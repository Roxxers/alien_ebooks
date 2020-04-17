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
import { MarkovPost, SubredditMarkovEndpoint, SubredditBuildRequest, TaskResponse } from "./endpoints";

import "../sass/bulma.scss";


const API_ROOT: string = "/api/v1";
const SUBREDDIT_ROOT: string = `${API_ROOT}/subreddits`;


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

async function requestSubredditCreation(url: string): Promise<void> {
    await makeBuildRequest(url)
        .then(taskID => {
            const buildURL = `${API_ROOT}/tasks/${taskID}`;
            let finished = false;
            const loadingBarContainer: HTMLElement = document.getElementById("LoadingBar");
            const bar = document.createElement("div");
            bar.innerHTML = `<progress id="downloading_percentage" class="progress is-primary" value="0" max="100">0%</progress>`;
            while (!finished) {
                let prog_per = fetch(buildURL)
                    .then(res => res.json() as Promise<TaskResponse>)
                    .then(data => {
                        const per = data.data.current / data.data.total
                        if (per >= 100) {
                            finished = true;
                        } else {
                            
                        }
                    });
            }
        });

}

async function makeBuildRequest(url: string): Promise<string> {
    const data = await fetch(url);
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
