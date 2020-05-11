import requests

def data_fetcher(url, savefile_name):
    """
    fetches data from external site
    TODO Try catch så der kan sendes true/false tilbage om download lykkedes
    """

    response = requests.get(url, savefile_name)

    # get the filename
    # fname = response.headers['Content-Disposition'].split('=')[1]

    # write content to file
    if response.ok:  # status_code == 200:
        with open(savefile_name, 'wb') as f:
            f.write(response.content)
    print('-----------------')
    print('Downloaded and saved to file {}'.format(savefile_name))

    return True