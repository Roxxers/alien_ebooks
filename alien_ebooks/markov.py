# alien_ebooks
# Copyright (C) 2019  Roxanne Gibson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Generates procedural posts, using markov chains and other methods."""

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
        for _ in range(amount):
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
