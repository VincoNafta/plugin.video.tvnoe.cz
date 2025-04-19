# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib.parse import urlencode
from urllib.parse import parse_qsl
import urllib3
import re

import xbmc
from bs4 import BeautifulSoup

import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'Z']

NOE_stream = "https://n106.quickmedia.tv/noetv/live/noetv/Ifd4_1_4/playlist.m3u8"
NOEplus_stream = "https://n106.quickmedia.tv/noetvplus/live/noetvplus/Shz3_1_1/playlist.m3u8"


user_agent = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}


def search(page):
    # user_agent = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}
    http = urllib3.PoolManager(10, headers=user_agent)
    return http.request("GET", page)


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Abecedni vyhledavani')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get video categories
    # Iterate through categories
    list_item = xbmcgui.ListItem(label='Noe ŽIVĚ')
    list_item.setInfo('video', {'title': 'NOE ŽIVĚ',
                                    'mediatype': 'video'})
    url = get_url(action='play_stream', stream=NOE_stream)
    list_item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, False)

    list_item = xbmcgui.ListItem(label='Noe+ ŽIVĚ')
    list_item.setInfo('video', {'title': 'NOE+ ŽIVĚ',
                                    'mediatype': 'video'})
    url = get_url(action='play_stream', stream=NOEplus_stream)
    list_item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    for category in ALPHABET:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        # list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
        #                   'icon': VIDEOS[category][0]['thumb'],
        #                   'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(start_character):
    """
    Create the list of playable videos in the Kodi interface.

    :param start_character: Category name
    :type start_character: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, start_character)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get the list of videos in the category.
    search_url = search("https://www.tvnoe.cz/videoteka/az/" + start_character).data
    raw_html = BeautifulSoup(search_url, "html.parser")
    # print(raw_html.prettify())
    shows = raw_html.find_all("div", class_="noe-porady-prehled-porad")
    # videos = get_videos(start_character)
    # Iterate through videos.
    for show in shows:
        # Create a list item with a text label and a thumbnail image.
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        show_name = \
            show.find("div", style="display:block; width: 100%;color: #424753;font-weight: bold;").text.split(":")[
                0].strip()
        show_image = show.find("div", style="margin-bottom: 1rem;")
        show_image = "https://www.tvnoe.cz" + show_image.img["src"]
        show_link = "https://www.tvnoe.cz/videoteka/hledej?search=" + show_name
        list_item = xbmcgui.ListItem(label=show_name)

        list_item.setInfo('video', {'title': show_name,
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': show_image, 'icon': show_image, 'fanart': show_image})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!

        # list_item.setProperty('IsPlayable', 'true')

        # Create a URL for a plugin recursive call.

        url = get_url(action='show_episodes', show_url=show_link)

        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_episodes(show_url):
    """
    Create the list of playable videos in the Kodi interface.

    :param start_character: Category name
    :type start_character: str
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Epizody')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Get the list of videos in the category.
    search_url = search(show_url).data
    raw_html = BeautifulSoup(search_url, "html.parser")
    # print(raw_html.prettify())
    searched_shows = raw_html.find("div", class_="noe-videoteka-prehled-porady")
    shows = searched_shows.find_all("a")
    # videos = get_videos(start_character)
    # Iterate through videos.
    for show in shows:
        # Create a list item with a text label and a thumbnail image.
        # Set additional info for the list item.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        show_name = show.find("div", style="display:block; width: 100%;color: #424753;font-weight: bold;").text
        show_image = show.find("div", style="margin-bottom: 1rem;")
        show_image = "https://www.tvnoe.cz" + show_image.img["src"]
        episode_url = "https://www.tvnoe.cz/" + show["href"]
        list_item = xbmcgui.ListItem(label=show_name)

        list_item.setInfo('video', {'title': show_name,
                                    'mediatype': 'video'})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': show_image, 'icon': show_image, 'fanart': show_image})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!

        list_item.setProperty('IsPlayable', 'true')

        # Create a URL for a plugin recursive call.

        url = get_url(action='play', video=episode_url)

        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    page_cn = search(path).data
    vp = BeautifulSoup(page_cn, "html.parser")

    # Find the div with class "container craplayer"
    v_raw_src = vp.find("div", class_="container craplayer")
    v_raw_src_html = v_raw_src.decode_contents()
    pattern = re.compile(r"src:\s*'([^']*\.m3u8)'")
    matches = pattern.findall(v_raw_src_html)

    play_item = xbmcgui.ListItem(path=matches[0])
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
def play_stream(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    xbmc.log(path)
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'show_episodes':
            # Display the list of videos in a provided category.
            list_episodes(params['show_url'])
        elif params['action'] == 'play_stream':
            play_stream(params['stream'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
