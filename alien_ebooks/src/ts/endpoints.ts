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

