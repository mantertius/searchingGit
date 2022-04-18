from datetime import datetime, time
from github import Github
# GITHUB TOKEN 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
ACCESS_TOKEN = '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'
#https://python.gotrained.com /search-github-api/
#https://pygithub.readthedocs.io

g = Github(ACCESS_TOKEN)


def search_github(keywords:list):
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaiming. Reset time: {rate.reset}')
        return
    else:
        print(f'\nYou have {rate.remaining}/{rate.limit} API calls remaining.')

    query_options = 'is:closed label:bug,defect linked:pr'
    query = '+'.join(keywords) + query_options
    result = g.search_issues(query,sort='updated',order='desc')
    print(f'Found {result.totalCount} issue(s).')
    now = datetime.now()
    filename = now.strftime("%m-%d-%Y %Hh%Mm%Ss")
    file = open(f"{filename}.txt",'w+')
    file.write(f'Query: {keywords[0]}\nQuery options: {query_options}\nResults: {result.totalCount}\n-----------------------\nurl | comments | stargazers\n')
    count = 0
    try:
        for issue in result:
            print(f'[{count}] {issue.html_url} | {issue.comments} comments | {issue.repository.stargazers_count} stargazers ')
            file.write(f'{issue.html_url} | {issue.comments} | {issue.repository.stargazers_count}\n')
            count+=1
    except:
        print('You have exceeded a secondary rate limit. Please wait a few minutes before you try again.')
    
    file.close()

if __name__ == '__main__':
    keywords = input('Enter keyword and separate them with \',\': ')
    keywords = [keywords.strip() for keyword in keywords.split(',')]
    print(f'Searching for: {keywords[0]}.')
    search_github(keywords)