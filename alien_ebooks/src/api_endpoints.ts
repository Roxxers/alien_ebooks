
export interface SubredditEndpoint {
    response_code: number;
    message: string;
    data: SubredditData;
}

export interface SubredditData {
    name: string;
    number_of_titles: number;
}

export interface SubredditMarkovEndpoint {
    response_code: number;
    message: string;
    data: string[];
}

export interface SubredditBuildRequest {
    response_code: number;
    message: string;
    data: BuildData;
}

export interface BuildData {
    task_id: string;
}
