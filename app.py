from agno.agent import Agent 
from agno.models.mistral import MistralChat
from agno.os import AgentOS
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools
# from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.youtube import YouTubeTools
from agno.tools.gmail import GmailTools
from agno.db.in_memory import InMemoryDb
from agno.tools.local_file_system import LocalFileSystemTools
from agno.team import Team
from dotenv import load_dotenv
from pathlib import Path

# load api key 
load_dotenv()

# define the path to save the research paper
dir_path = Path("./research_papers/")
dir_path.mkdir(exist_ok=True)

# define the dir to save the generated medium articles
target_dir = Path("./medium_articles/")
target_dir.mkdir(exist_ok=True)


# define orchestrator and agent model
orchestrator_model = MistralChat(id="mistral-large-latest")
model = MistralChat(id="mistral-large-latest")

# create db for the team leader
db = InMemoryDb()

# ========================Agents=======================
# define my members of the team 

#  define Arxiv research Agent
arxiv_research_agent = Agent(
    id = "arxiv-research-agent",
    name="Archive Research Agent",
    model=model,
    role="Arxiv Research Assistant",
    instructions=["You are a research Agent that gathers research papers from arxiv",
                  "use the available tools to search the papers,authors and topics as per user suggestion",
                  "summerize your result in a clear and consise way"],
    tools=[ArxivTools(download_dir=dir_path)],
    add_datetime_to_context=True
)

# Web Search Agent Dugduggo and goggle search 

web_search_agent = Agent(
    id="web_search_agent",
    name="Web Search Agent",
    model=model,
    role="Web Research Assistant",
    instructions=["You are aresearch assistant that gathers infromation from the web",
                  "use the available tools to search for article,summary and other important material based on the top of user request",
                  "summerize your findings along with the resource links"],
    add_datetime_to_context=True,
    tools=[DuckDuckGoTools()]

)

#define the Hackernews Research Agent

hackernews_research_agent = Agent(
    id = "hackernews-earch-agent",
    name="HackerNews search Agent",
    role="HackerNews Research Assistant",
    model=model,
    instructions=["You are an expert research assistant that can access hackernews",
                  "get relevent informations for the recent topics, and get information about the articles for the topic user requested for",
                  "Summerize your finding in proper format"],
    add_datetime_to_context=True,
    tools=[HackerNewsTools()]
)

# define Newspaper4k Agent
news_article_research_agent = Agent(
    id="news-article-research-agent",
    name="News Article Research Agent",
    model=model,
    role="News Article Research Agent",
    instructions=["You are a research assistant that can read the contents of articles",
                  "Whenever an url is provided you can read the content of the article and can also get its data",
                  "Using the available tools search for articles and summarize them and gather relevant information"],
    add_datetime_to_context=True,
    tools=[Newspaper4kTools(include_summary=True)]
)

# define the wikipedia tool
wikipedia_research_agent = Agent(
    id="wikipedia-research-agent",
    name="Wikipedia Research Agent",
    role="Wikipedia Research Assistant",
    model=model,
    instructions=["You are a research assistant that gathers information from Wikipedia based on the input topic",
                  "You have the capability to search for articles and gather its content",
                  "Summarize the findings and mention the appropriate resources and references in your output"],
    add_datetime_to_context=True,
    tools=[WikipediaTools()]
)
 

# youtube research agent
youtube_research_agent = Agent(
    id="youtube-research-agent",
    name="Youtube Research Agent",
    model=model,
    role="Youtube Research Assistant",
    instructions=["You are a research assistant that gathers information from Youtube",
                  "You have the capability to read youtube video transcripts and summarize them",
                  "You can also read metadata related to youtube videos",
                  "you can also fetch timestamps of a particular video",
                  "summarize the transcripts in clear and concised manner"],
    add_datetime_to_context=True,
    tools=[YouTubeTools()]
)


# reddit research agent
# reddit_research_agent = Agent(
#     id="reddit-research-agent",
#     name="Reddit Research Agent",
#     model=model,
#     role="Reddit Research Assistant",
#     instructions=["you are a research assistant that gathers information from Reddit",
#                   "You have access to read posts and also gather data for subreddits",
#                   "you can also gather the latest posts from reddit"],
#     add_datetime_to_context=True,
#     tools=[RedditTools()]
# )


# gmail agent
gmail_agent = Agent(
    id="gmail-agent",
    name="Gmail Agent",
    role="Manages mails through Gmail",
    instructions=["You are a helpful agent that can draft messages using gmail",
                  "you have the capability to draft mails, read mails and send mails whenever requested by the user",
                  "you have the capability to search for mails and read them",
                  "make sure to always confirm the drafted before sending it to the mail id",
                  "make sure to write the mails in proper format including a relevant subject line"],
    model=model,
    add_datetime_to_context=True,
    tools=[GmailTools(port=8000)]
)



# ======================== Team =================================


medium_article_team = Team(
    id="medium-article-creation-team",
    name="Medium Article Creation Team",
    role="Team Leader which manages research and content creation",
    db=db,
    members=[arxiv_research_agent,
             web_search_agent,
             hackernews_research_agent,
             news_article_research_agent,
             wikipedia_research_agent,
             youtube_research_agent,
             gmail_agent],
    model=orchestrator_model,
    instructions=["You are a team leader managing multiple sub agents in your team",
                  "You have access to agents which can do research based on the topic on various sources such as arxiv, youtube, wikipedia, hackernews, newspaper articles, web search using google search and duckduckgo search",
                  "you also have the capability to read and write emails",
                  "your task is to understand the topic given by the user and fetch relevant research information using your team members",
                  "once you have enough research material, your primary task is to create medium(platform) styled articles",
                  "for checking how articles are written on medium you can use the article research agent",
                  "once you have created the medium article, show the user the final draft",
                  "only when the user confirms the draft, save it to the filesystem in a markdown format as a .md file using the filename suggested by user",
                  "if the user does not give a filename, then use a self created name based on the topic on which the article was created"],
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=10,
    tools=[LocalFileSystemTools(target_directory=target_dir,
                                default_extension="md")],
    stream=True,
    markdown=True
)


# ======================== AgentOS ============================

agent_os = AgentOS(
    id="medium-article-os",
    name="Medium Article Generator OS",
    description="An Agent that conducts research of latest tech topics across multiple platforms and generates medium articles based on its findings",
    teams=[medium_article_team]
)


# create a fastapi app
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(
        app="app:app",
    )