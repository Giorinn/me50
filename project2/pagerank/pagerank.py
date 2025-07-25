import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    # init dict and compute the probability of transition by choosing a random page from corpus
    prob_dict = {key: (1 - damping_factor) / len(corpus) for key in corpus}
    links = corpus[page]
    link_num = len(links)

    # compute the probability of transition by links
    if link_num != 0:
        link_possibility = damping_factor / link_num
        for link_page in links:
            prob_dict[link_page] += link_possibility

    return prob_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # init page_rank and generate start page
    current_page = random.choice(list(corpus.keys()))
    rank_dict = {key: 0.0 for key in corpus}
    rank_dict[current_page] += 1

    # generate samples
    for i in range(n - 1):
        prob_dict = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(prob_dict.keys()), weights=list(prob_dict.values()), k=1)[0]
        rank_dict[next_page] += 1
        current_page = next_page

    for key in rank_dict:
        rank_dict[key] /= n
    return rank_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_num = len(corpus)
    rank_dict = {key: 1 / page_num for key in corpus}
    precision = 0.001
    dangling_pages = [page for page in corpus if len(corpus[page]) == 0]

    while True:
        new_rank_dict = {}
        max_diff = 0
        dangling_pr = sum(rank_dict[page] for page in dangling_pages)


        for target_page in corpus:
            pr = (1 - damping_factor) / page_num + damping_factor * dangling_pr / page_num

            for source_page in corpus:
                if target_page in corpus[source_page]:
                    pr += damping_factor * rank_dict[source_page] / len(corpus[source_page])

            diff = abs(pr - rank_dict[target_page])
            max_diff = max(diff, max_diff)
            new_rank_dict[target_page] = pr

        if max_diff <= precision:
            break
        rank_dict = new_rank_dict

    return rank_dict

if __name__ == "__main__":
    main()
