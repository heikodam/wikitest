import web_scraper
# import sys

def is_link_in_page(page_to_check, end_link):
    links_on_page = web_scraper.getAllUrl(page_to_check)
    if end_link in links_on_page:
        return True
    else:
        return False

#get all links for n degree higher
def get_all_degree_links(degree, start_degree_pages, end_link):
    current_degree_pages = []
    #if no more degrees to go return all links of current degree
    if degree == 0:
        return start_degree_pages
    #for each page in current degree get all URLS
    for page in start_degree_pages:
        all_pages = web_scraper.getAllUrl(page)
        #if end link found return
        if end_link in all_pages:
            return list(current_degree_pages) + list(all_pages)
        current_degree_pages += all_pages
    #do some for next degree
    return get_all_degree_links(degree - 1, current_degree_pages, end_link)




def degree_distance(start_link, end_link):
    #this is the path to start with
    path = [[start_link]]

    #check if they are 0 degrees away
    # if start_link == end_link:
    #     print("They are the same")
    #     sys.exit()

    #start with 1 degree
    degree_count = 1
    #Search until the end link is found
    while True:
        #get all links of one degree higher
        path.append(get_all_degree_links(1, path[degree_count - 1], end_link))
        #check if link in that degree
        if end_link in path[degree_count]:
            print("They are {} clicks away".format(degree_count))
            return degree_count
        degree_count += 1