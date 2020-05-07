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


export const loadingBar: HTMLElement = document.getElementById("downloading_percentage");

export async function updateLoadingBar(task): Promise<void> {
    if (task.state === "FINISHED") {
        loadingBar.classList.add("is-hidden");
        // Do something before delay
        // await requestTitles(task.subreddit);
        // Do something after
    } else {
        let percent: number;
        percent = (task.current / task.total) * 100;
        percent = Math.round(percent);
        console.log("Percent complete: ", percent);
        loadingBar.setAttribute("value", percent.toString());
    }
}
