

function refresh_titles(amount:number) {
    var request = new XMLHttpRequest()

    request.open('GET', 'http://127.0.0.1:5000/api/v1/subreddit/gaysoundsshitposts/markov?amount=1', true)
    
    request.onload = function() {
        var title = document.getElementById('gen')
        var data = JSON.parse(this.response)
        title.innerHTML = data
    }
    
    request.send()
}
