import pandas as pd

# This URL will work on a local Jupyter Notebook.
# url="https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

# Here we'll use a local copy instead.
# Use the local copy instead.
url = "https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/Bills_Lists/Details_page?blsId=legislation%2fbillslst%2fbillslst_c203aa1c-1876-41a8-bc76-1de328bdb726"

table = pd.read_html(url, header=0)[0]

print(table.head())
