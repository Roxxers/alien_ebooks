
import markovify
from pony.orm import db_session
from subredditgenerator import cache


class MarkovGenerator:

    def __init__(self, subreddit_entity):
        self.subreddit = subreddit_entity
        self.titles = "\n".join(self.subreddit.titles.title)
        self.cache = cache.Cache()
        
    def _get_markov_cache(self):
        return self.cache.get(self.subreddit.name)
    
    def _cache_markov_chain(self, markov_chain):
        return self.cache.set(self.subreddit.name, markov_chain)
    
    def _make_markov_chain(self):
        return markovify.NewlineText(self.titles, well_formed=False, state_size=2)
    
    @db_session
    def generate_sentences(self, amount=1):
        max_amount = 20
        amount = amount if amount <= max_amount else max_amount  # Only allow a max of 20 to be generated
        
        cached_chain = self._get_markov_cache()
        
        if not cached_chain:
            chain = self._make_markov_chain()
            self._cache_markov_chain(chain)
        else:
            chain = cached_chain
        
        return [chain.make_sentence() for x in range(amount)]
