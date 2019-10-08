
export interface SubredditEndpoint {
    response_code: number;
    message: string;
    data: Data;
}

export interface Data {
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
    data: Data;
}

export interface Data {
    task_id: string;
}
