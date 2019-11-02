
export interface hewwo {
}

export interface SubredditEndpoint {
    response_code: number;
    message: string;
    data: SubredditData;
}

export interface SubredditData {
    name: string;
    number_of_titles: number;
}

export interface MarkovPost {
    title: string;
    comments: number;
    nsfw: boolean;
    subreddit: string;
}

export interface SubredditMarkovEndpoint {
    response_code: number;
    message: string;
    data: MarkovPost[];
}

export interface BuildData {
    task_id: string;
}

export interface SubredditBuildRequest {
    response_code: number;
    message: string;
    data: BuildData;
}

