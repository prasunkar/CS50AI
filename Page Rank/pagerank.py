import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 100000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dist = dict()

    if corpus[page]:
        for link in corpus:
            dist[link] = (1 - damping_factor) / len(corpus)
            
            if link in corpus[page]:
                dist[link] += damping_factor / len(corpus[page])
    
    else:
        # Randomly choose a page if no links are found
        for link in corpus:
            dist[link] = 1 / len(corpus)

    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    # Initialize first sample with None
    sample = None

    for page in corpus:
        # Initialize empty values
        pagerank[page] = 0

    for _ in range(n):
        if sample is None:
            # First sample is always random
            sample = random.choice(list(corpus.keys()))
        
        else:
            # Generate new sample based on the previous sample's transition model
            model = transition_model(corpus, sample, damping_factor)
            population, weights = zip(*model.items())
            sample = random.choice(random.choices(population, weights=weights))

        pagerank[sample] += 1

    for page in corpus:
        pagerank[page] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    newrank = dict()

    # Assign initial values
    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    loop = True

    while loop:
        # Calculate newrank values based on all current pagerank values
        for page in pagerank:
            total = 0

            for possible_page in corpus:
                # Keep all linked-to possible pages in mind
                if page in corpus[possible_page]:
                    total += pagerank[possible_page] / len(corpus[possible_page])
                
                if not corpus[possible_page]:
                    total += pagerank[possible_page] / len(corpus)

            newrank[page] = (1 - damping_factor) / len(corpus) + damping_factor * total

        # Break the loop once we're finished
        loop = False

        # If any of the values changes by more than the threshold, start the loop again
        for page in pagerank:
            if not math.isclose(newrank[page], pagerank[page], abs_tol=0.001):
                loop = True
            
            # Assign new values to current values
            pagerank[page] = newrank[page]

    return pagerank


if __name__ == "__main__":
    main()