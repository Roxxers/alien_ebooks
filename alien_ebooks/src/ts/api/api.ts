

import * as endpoints from "./endpoints";

export async function makeBuildRequest(subreddit: string): Promise<string> {
    const url = `${endpoints.API_ROOT}/subreddits/${subreddit}`;
    const data = await fetch(url, {method: "POST"});
    const res = await (data.json() as Promise<endpoints.SubredditBuildRequest>);
    return res.data.task_id;
}

export async function checkSubredditExists(subreddit: string): Promise<boolean> {
    const url: string = `${endpoints.SUBREDDIT_ROOT}/${subreddit}`;
    return fetch(url)
        .then(res => {
            if (res.status === 200) {
                return true;
            } else if (res.status === 404) {
                return false;
            } else {
                throw new Error("checkSubredditExists API returned neither 200 or 404");
            }
        });
}

export async function requestTitles(subreddit: string): Promise<endpoints.SubredditMarkovEndpoint> {
    const url: string = `${endpoints.SUBREDDIT_ROOT}/${subreddit}/markov?amount=5`;
    return fetch(url)
        .then(async res => {
            return await res.json() as endpoints.SubredditMarkovEndpoint;
        });
}
