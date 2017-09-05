# -*- coding: utf-8 -*-

"""
Tarbell project configuration
"""

from flask import Blueprint, Response, g
import datetime
# import xlrd.xldate
import xlrd
import random
import jinja2


# imports bc copied blueprint functions #
from clint.textui import colored
import p2p
from tarbell.utils import puts
from tarbell.oauth import get_drive_api
from tarbell.hooks import register_hook


from collections import OrderedDict
from jinja2 import Markup
from jinja2.exceptions import TemplateNotFound
import re, codecs, archieml

from pprint import pprint
from apiclient import errors
# from flask import Blueprint, Response, g

from subprocess import call

blueprint = Blueprint('lake-michigan-water-stories', __name__)
CONTENT_ITEMS_WORKSHEET = 'p2p_content_items'

############################
# text and other formatting filters #
############################

@blueprint.app_template_filter('xldate_to_datetime')
def xldate_to_datetime(xldate):
    return xldate
    if isinstance(xldate, unicode):
        print('unicode!!')
        retval = datetime.datetime.strptime(xldate, '%m/%d/%Y')
    else:
        print('Not unicode!!')
        retval = xlrd.xldate.xldate_as_datetime(xldate, 0)
        # retval = xldate_as_tuple(xldate, 0)
    return retval

@blueprint.app_template_filter('format_date')
def format_vote_date(date_to_format, format):
    return date_to_format.strftime(format)


############################
# ASSET EMBEDDING AND INTEGRATION #
############################


@blueprint.app_template_filter('get_video_ref')
def get_video_ref(url):
    """
    plucks a needed reference # from the video url
    """
    retval = url.split("/")
    ref_index = retval.index("videogallery") + 1
    return retval[ref_index]

@blueprint.app_template_filter('generate_id')
def generate_id(number):
    rando = random.random()
    return "myExperience {}".format(rando)

@blueprint.app_template_filter('check_if_is_okay_to_publish')
# @jinja2.contextfilter
def check_if_is_okay_to_publish(photo):
    """
    Takes a p2p data dict and determines if it is okay to publish this content item. It will return true
    in all cases except when the content is not set to Live and the publish url is the production bucket
    """
    # TODO: Make this work!
    return True

@blueprint.app_template_filter('strip_whitespace')
# @jinja2.contextfilter
def strip_whitespace(text):
    """
    Removes leading and trailing whitespace 
    """
    return text.strip()

@blueprint.app_template_filter('find_inline_link')
def find_inline_link(words):
    """
    Looks for '{{ ROOT URL }}' and return the actual root url
    """
    return words.replace('{{ ROOT_URL }}', DEFAULT_CONTEXT['ROOT_URL'])


@blueprint.app_template_filter('dumb_to_smart_quotes')
def dumb_to_smart_quotes(string):
    """
    Takes a string and returns it with dumb quotes, single and double,
    replaced by smart quotes. Accounts for the possibility of HTML tags
    within the string.

    https://gist.github.com/davidtheclark/5521432
    """

    # Find dumb double quotes coming directly after letters or punctuation,
    # and replace them with right double quotes.
    string = re.sub(r'([a-zA-Z0-9.,?!;:\'\"])"', r'\1&#8221;', string)
    # Find any remaining dumb double quotes and replace them with
    # left double quotes.
    string = string.replace('"', '&#8220;')
    # Reverse: Find any SMART quotes that have been (mistakenly) placed around HTML
    # attributes (following =) and replace them with dumb quotes.
    string = re.sub(r'=&#8220;(.*?)&#8221;', r'="\1"', string)
    # Follow the same process with dumb/smart single quotes
    string = re.sub(r"([a-zA-Z0-9.,?!;:\"\'])'", r'\1&#8217;', string)
    string = string.replace("'", '&#8216;')
    string = re.sub(r'=&#8216;(.*?)&#8217;', r"='\1'", string)
    return string


############################
# OTHER UTILITIES FOR THE STORIES #
############################


@blueprint.app_template_filter('get_up_next')
def get_up_next(parts, current_part):
    """
        Takes the entire dict of story parts (day1, day2, etc.) and the current story part (part1, part2 , etc).
        It finds the next story and stashes it inside the retval with it's own key. the rest of the parts
        are put into retval['rest'] 
        
    """
    retval = {}
    for i in range(0, len(parts)):
        if parts[i]['part'] == current_part:
            try: 
                retval['next'] = parts[i+1]
                del parts[i+1]
                retval['rest'] = parts
                break
            except IndexError:
                # This exception exists incase there is no up next, in which case there would be an index error
                retval['next'] = False
                retval['rest'] = parts
    return retval


############################
# this is the archiml stuff #
############################

# Google document key for the stories
DOC_KEY = '1h-1NS3bggsPAxaI2oulQZ7B-WnucTRUbEYsHBRPEWko'

# @register_hook('preview')
# @register_hook('generate')
# def get_drive_api_stuff(site):
#     service = get_drive_api()
#     try:
#         docfile = service.files().get(fileId=DOC_KEY).execute()
#         downloadurl = docfile['exportLinks']['text/html'] # export as 'text/html' instead of 'text/plain' if we want to parse links and styles
#         resp, content = service._http.request(downloadurl)

#         # write to file
#         with open('out_drive.html', 'w+') as f:
#             text = content.decode("utf-8-sig", errors='ignore') # get rid of BOM
#             f.write(text.encode('utf8', 'replace')) # lol
#         return text
#     except errors.HttpError, error:
#         print 'An error occurred: %s' % error

# get_drive_api_stuff(False)

def get_extra_context():
    print ">>>>> PARSING NEW STORY"
    call(["node", "scripts/js_parser.js", "out_drive.html"]) # parse the html before loading it into archieML
    with open('./out_parsed.txt') as f:
        data = archieml.load(f)
    data = dict(data)
    return data

@blueprint.app_template_filter()
def add_ptags(text):
    p_text = '<p>'+text; # opening p
    p_text = p_text.replace('\n', '</p><p>') + '</p>' # closing p
    return Markup(p_text)

@blueprint.app_template_filter()
def format(title):
  return title.replace('-', ' ').capitalize()

@blueprint.app_template_filter()
def lower(filename):
  return filename.lower()

############################
# copied from blueprint.py #
############################

def _get_published_content(site, s3, **extra_context):
    template = site.app.jinja_env.get_template('_content.html')
    context = site.get_context(publish=True)
    context.update(extra_context)
    rendered = template.render(**context)

    return rendered

def p2p_publish_archiemlstory(site, s3):
    if not is_production_bucket(s3.bucket, site.project.S3_BUCKETS):
        puts(colored.red(
            "\nNot publishing to production bucket. Skipping P2P publiction."))
        return

    context = site.get_context(publish=True)

    # Handle old-style configuration for publishing HTML story from values
    # worksheet. This is deprecated, but still support it in case someone
    # accidentally upgrades their blueprint in an old project
    try:
        content_item = get_deprecated_htmlstory_config(context)
        msg = ("\nYou've configured your HTML story in the 'values' worksheet. "
                "Don't do this. It will work for now, but may stop working "
                "soon. Instead, configure it in the 'p2p_content_items' "
                "worksheet.")
        puts(colored.red(msg))
        p2p_publish_htmlstory(content_item, site, s3)

    except KeyError:
        # This is fine. Actually preferred. There shouldn't be anything
        # P2P-related
        pass

    try:
        content_items = context[CONTENT_ITEMS_WORKSHEET]
    except KeyError:
        # No worksheet with the P2P content item configuration.  Fail!
        msg = ("\nYou need a worksheet named {0} in your Tarbell spreadsheet "
               "to publish P2P content items").format(CONTENT_ITEMS_WORKSHEET)
        puts(colored.red(msg))
        return

    for i, content_item in enumerate(content_items):
        try:
            content_type = content_item['content_type']
        except KeyError:
            msg = ("\nYou need to specify a content type for P2P content "
                    "item {0}").format(i)
            continue

        try:
            if content_type == 'blurb':
                p2p_publish_blurb(content_item, site, s3)

            elif content_type == 'htmlstory':
                p2p_publish_htmlstory(content_item, site, s3)

            else:
                msg = ("\nUnknown content type '{0}' for P2P content "
                       "item {1}. Skipping publication.").format(content_type, i)
                puts(colored.yellow(msg))
                continue

        except MissingP2PContentItemFieldError as e:
            # The spreadsheet is missing a field needed to publish. Fail
            # gracefully.
            msg = ("\nYou need to specify field '{0}' for P2P content "
                    "item {1}. Skipping publication.").format(e.field_name, i)
            puts(colored.yellow(msg))
            continue

        except TemplateNotFound:
            msg = ("\nCould not find template '{0}' for P2P content "
                   "item {1}. Skipping publication").format(
                       content_item['template'], i)
            puts(colored.yellow(msg))
            continue


# Google spreadsheet key
SPREADSHEET_KEY = "1F8yvZm2awwsRycdV_nzywlaoT_xUjvYcpOoGfye8CZw"

# Exclude these files from publication
EXCLUDES = ['*.md', 'scripts', 'requirements.txt', 'node_modules', 'sass', 'js/src', 'package.json', 'Gruntfile.js', 'subtemplates']

# Spreadsheet cache lifetime in seconds. (Default: 4)
# SPREADSHEET_CACHE_TTL = 4

# Create JSON data at ./data.json, disabled by default
# CREATE_JSON = True

# Get context from a local file or URL. This file can be a CSV or Excel
# spreadsheet file. Relative, absolute, and remote (http/https) paths can be 
# used.
# CONTEXT_SOURCE_FILE = ""

# EXPERIMENTAL: Path to a credentials file to authenticate with Google Drive.
# This is useful for for automated deployment. This option may be replaced by
# command line flag or environment variable. Take care not to commit or publish
# your credentials file.
# CREDENTIALS_PATH = ""

# S3 bucket configuration
S3_BUCKETS = {
    # Provide target -> s3 url pairs, such as:
    #     "mytarget": "mys3url.bucket.url/some/path"
    # then use tarbell publish mytarget to publish to it
    
    "production": "graphics.chicagotribune.com/news/lake-michigan-water-stories",
    "staging": "apps.beta.tribapps.com/lake-michigan-water-stories",
}

# Default template variables
DEFAULT_CONTEXT = {
   'OMNITURE': {   'domain': 'chicagotribune.com',
                    'section': 'news',
                    'sitename': 'Chicago Tribune',
                    'subsection': 'local',
                    'subsubsection': '',
                    'type': 'dataproject'},
    'name': 'lake-michigan-water-stories',
    'title': 'Lake Michigan Water Stories'
}

@register_hook('preview')
@register_hook('generate')
def update_context(site):
    DEFAULT_CONTEXT.update(**get_extra_context())

@register_hook('preview')
@register_hook('generate')
def get_drive_api_stuff(site):
    print ">>>>> GETTING NEW STORY TEXT"
    service = get_drive_api()
    try:
        docfile = service.files().get(fileId=DOC_KEY).execute()
        downloadurl = docfile['exportLinks']['text/html'] # export as 'text/html' instead of 'text/plain' if we want to parse links and styles
        resp, content = service._http.request(downloadurl)

        # write to file
        with open('out_drive.html', 'w+') as f:
            text = content.decode("utf-8-sig", errors='ignore') # get rid of BOM
            f.write(text.encode('utf8', 'replace')) # lol
        return text
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

    DEFAULT_CONTEXT.update(**get_extra_context())


# Make the archiemal thing auto

# @register_hook('preview')
# @register_hook('generate')
# def copy_assets(site, output_root=None, extra_context=None):
#     """Copy assets in non-standard directories to a more logical place"""
#     # Check if we've already done this to avoid slow filesystem checks
#     # on every request
#     t