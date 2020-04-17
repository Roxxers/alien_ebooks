
import { MarkovPost } from "./endpoints";

/**
 * Creates element that fits with the bulma framework
 * @param tag - html tag for element
 * @param classes - list of space separated classes to add to the element
 * @returns Bulma HTML Element
 */
function createElementWithClasses(tag: string, classes: string): HTMLElement {
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
    const article = createElementWithClasses("article", "media");
    // Media-left, image placeholder
    const mediaImage = createElementWithClasses("div", "media-left");
    const image = createElementWithClasses("div", "placeholder");
    image.innerHTML = `<span class="icon"><i class="fas fa-quote-left placeholder-icon"></i></span>`;
    mediaImage.appendChild(image);
    // Media Content
    const mediaContent = createElementWithClasses("div", "media-content");
    const contentWrapper = createElementWithClasses("div", "content");
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
export function createTitleElements(posts: MarkovPost[]): HTMLElement[] {
    const articles: HTMLElement[] = [];
    posts.forEach(post => {
        const article = createMediaElement();
        const contentElement = document.createElement("p");

        let title = `<strong>${post.title}</strong>`;
        if (post.nsfw) {
            title += ` <span class="nsfw">NSFW</span>`;
        }

        const postMetaLine = `<span class="has-text-grey is-size-7"><strong>r/${post.subreddit}</strong> by u/exampleuser`;
        const commentsCounter = `<span class="icon"><i class="fas fa-comment-alt"></i></span> ${post.comments} Comments</span>`;


        contentElement.innerHTML = `${title}<br>${postMetaLine}<br>${commentsCounter}`;
        const mediaContent = article.getElementsByClassName("media-content");
        mediaContent[0].children[0].appendChild(contentElement);
        articles.push(article);
    });
    return articles;
}
