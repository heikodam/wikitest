import web_scraper
import sys

def is_link_in_page(page_to_check, end_link):
    links_on_page = web_scraper.getAllUrl(page_to_check)
    if end_link in links_on_page:
        return True
    else:
        return False

#get all links for n degree higher
def get_all_degree_links(degree, start_degree_pages):
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
        elif end_link in reverse_path[-1]:
            print("Path Found here")
            return 
        current_degree_pages += all_pages
    #do some for next degree
    return get_all_degree_links(degree - 1, current_degree_pages)


def get_all_reverse_degree_links(degree, start_degree_pages):
    current_degree_pages = []
    #if no more degrees to go return all links of current degree
    if degree == 0:
        return start_degree_pages
    #for each page in current degree get all URLS
    for page in start_degree_pages:
        all_pages = web_scraper.getAllBackLinks(page)
        current_degree_pages += all_pages
    #do some for next degree
    return get_all_degree_links(degree - 1, current_degree_pages)


#set the start and end wiki page title
start_link = "Flour"
end_link = "Sovereign_state"
#this is the path to start with
path = [[start_link]]
reverse_path = [[end_link]]

#check if they are 0 degrees away
if start_link == end_link:
    print("They are the same")
    sys.exit()

#start with 1 degree
degree_count = 1



while True:
    print("Calling path")
    path.append(get_all_degree_links(1, path[degree_count - 1]))
    #check if link in that degree
    if end_link in path[degree_count]:
        print("One Direction")
        print("They are {} clicks away".format(degree_count))
        break
    
    print("Calling reverse_path")
    reverse_path.append(get_all_reverse_degree_links(1, reverse_path[degree_count - 1]))

    degree_count += 1

    overlap = set(path[degree_count - 1]) & set(reverse_path[degree_count - 1])
    if len(overlap) > 0:
        print("Both Directions")
        print("They are {} clicks away".format(len(path) + len(reverse_path) - 2))
        break

    


#Search until the end link is found

#get all links of one degree higher
#path.append(get_all_degree_links(1, path[degree_count - 1]))
# #check if link in that degree
# if end_link in path[degree_count]:
#     print("They are {} clicks away".format(degree_count))

# reverse_path.append(get_all_reverse_degree_links(1, reverse_path[degree_count - 1]))
# degree_count += 1


# overlap = set(path[degree_count - 1]) & set(reverse_path[degree_count - 1])
# print(path[degree_count - 1])
# print(reverse_path[degree_count - 1])
# if len(overlap) > 0:
#     print("They are {} clicks away".format(len(path) + len(reverse_path) - 2))