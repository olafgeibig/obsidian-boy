Add the requirement that the webscraper should scrape a webpage to markdown.
Let's add a chapter that defines the responsibilities of the classes and the purpose of their methods. Here are my bullet points, write them properly and add what I missed, add responsibilities for the methods that I missed:
# ObsidianInterface
Interfaces with Obsidian notes via the file system. Simply CRUD on the markdown files. Knows the Vault directory
## list_daily_notes
list all daily note files
# DailyNoteProcessor
Extracts the data from the daily notes into a data structure and fills the gaps in the data. 
## extract_entries
parses the daily notes and extracts the entries with an LLM
## fill_gaps
Use the researcher to research the missing fields of a daily note entry
# Researcher
An AI research agent that performs high level research tasks for specific use cases. It can do websearches and scrape webpages
## research_entry
Takes an entry and researches the missing information
#WebScraper
Scrapes the content of a website into a markdown document
# MemoryManager
Has a knowledge base that it can store information with and retrieve from it