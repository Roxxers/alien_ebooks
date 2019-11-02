import random

import markovify


class MarkovGenerator:
    def __init__(self, subreddit_entity, cache):
        self.subreddit = subreddit_entity
        self.titles = "\n".join(self.subreddit.titles.title)
        self.cache = cache

    def _get_markov_cache(self):
        return self.cache.get(self.subreddit.name)

    def _cache_markov_chain(self, markov_chain):
        return self.cache.set(self.subreddit.name, markov_chain)

    def _make_markov_chain(self):
        return markovify.NewlineText(
            self.titles, well_formed=False, state_size=2
        )

    def generate_sentences(self, amount=1):
        max_amount = 20
        amount = amount if amount <= max_amount else max_amount # Only allow a max of 20 to be generated

        cached_chain = self._get_markov_cache()

        if not cached_chain:
            chain = self._make_markov_chain()
            self._cache_markov_chain(chain)
        else:
            chain = cached_chain

        posts = []
        for x in range(amount):
            title = chain.make_sentence()
            no_comments = [
                title.number_of_comments for title in self.subreddit.titles
            ]
            comments = random.randint(min(no_comments), max(no_comments))
            is_nsfw = bool(self.subreddit.nsfw_percentage > random.random())
            post = {
                "title": title,
                "comments": comments,
                "nsfw": is_nsfw,
                "subreddit": self.subreddit.name
            }
            posts.append(post)

        return posts
