# Lake Michigan Water Disparity stories

A [Tarbell](http://tarbell.io) project.

#TODO:

    - Lazyload the galleries
    - Somehow mobileize the header background images.

IN BRIEF
--------

This project was built to deliver the complete Lake Michigan Water stories. It pulls content from [Google Docs](https://docs.google.com/document/d/1h-1NS3bggsPAxaI2oulQZ7B-WnucTRUbEYsHBRPEWko/edit#), [Google Spreadsheets](https://docs.google.com/spreadsheets/d/1F8yvZm2awwsRycdV_nzywlaoT_xUjvYcpOoGfye8CZw/edit#gid=58965968) and other tarbell projects and synthesizes it all into the final set of stories.

This is the second outing for this rig.

HOW IS IT CONSTRUCTED
---------------------

This project uses the old News Apps bootstrap blueprint, but most of that has been excised. There is very little bootstrap left. The blueprint's `_base.html` is extended by this project's `_project-base.html`. Here lives all the stuff common to all stories including the universal `app.js` which governs lazy loading of graphics and photos using the npm package [In-View](https://www.npmjs.com/package/in-view).


THE STORIES AND THEIR ASSETS
----------------------------

As mentioned before, the primary driver is the `_project-base.html`. Each individual story gets its own template extension of the tax base. Here, all the story-specific information is pulled in here, much of it governed by a variable `part` (e.g. part = "appeals") set at the top of each template. The potential values for the part variable are:

    - Part 1 TK
    - Part 2 TK
    - Part sidebar TK

Throughout the spreadsheet tabs are content specific to each story, and the keys are uniformly prefixed with these values. For example, the seo description for each story is found in the spreadsheet under the key `<part>_seo_description`. 

The actual stories are fed into this rig from a Google Docs](https://docs.google.com/document/d/1h-1NS3bggsPAxaI2oulQZ7B-WnucTRUbEYsHBRPEWko/edit#) using [Archie Markup Language](http://archieml.org/). Using the 'part' labels as mentioned above, the archieml is parsed into a single dictionary which is added to the tarbell project's context as `stories`.

Part 1: stories.assessents 
Part 2: stories.appeals 
Part 3: stories.houlihan 
...
etc.

The archieml is the blueprint for each story, and is divided into chunks. Each chunk is a content type (text, refer, photo, graphic, etc.) and is rendered in order using jinja macros (defined on `_tax-base.html` for each type. The template logic for this resides in the subtemplate `_story-loop` which reads the imported stories and outputs the content.

For our purposes here, the variable `s` will be a chunk of content.

STORY TEXT
==========

Like each content type, the defining property is s.type. For type "text", there is very little to do. If the optional `has_inline_link` is true, the text is first run through a custom filter which seeks the substring "{{ ROOT_URL }}" and replaces it with the actual ROOT_URL. That way, links in the story text to other pages will remain functional on local, beta and prod without any action.

Otherwise, all text is run through another custom filter to insert smart quotes and then the markdown filter.

Setting the boolean `close_river` to false will close the `<div.container>` before outputting the content, thus putting it at full width. Otherwise, the content item will be constricted to the narrow "river" defining this project's design. This attribute is available for all content items.

AML example:

    type: text
    has_inline_link: <True/False> (optional)
    close_river: <True/False> (optional)
    content: lorem ipsum Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quam magnam, delectus a numquam, maiores molestiae illo suscipit, eos asperiores debitis cumque vitae incidunt autem. Rerum corrupti tempora, doloremque. Labore, laborum?
    :end



GRAPHICS
========

Graphics are loaded in iFrames using the NPR-built [pym.js](https://github.com/nprapps/pym.js/). There are three primary tarbell repos which serve up graphics, and each repo/project must be published and republished seperately. The projects are:
    
    - (Most static graphics) https://tribune.unfuddle.com/git/tribune_property-tax-assessments-cook-county/
    - (Most interactives, including lookup, township and the over/under map) https://tribune.unfuddle.com/git/tribune_property-tax-assessments-map/
    - (The scatterplot) https://tribune.unfuddle.com/git/tribune_property-tax-assessments-broken-model-scatterplots/

Each graphic asset requires a type, unique id and url for the iframe. The optional `add_class` attribute simply takes the string provided and inserts it into the class attribute of the graphic's wrapper. This is available in most content types.

AML example:

    type: graphic
    graphic_id: <unique id>
    url: <url>
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


PHOTOS
======

Photos are pulled directly from p2p and require only a p2p slug. The booleans `display_caption` and `display_credit` can turn their corresponding elements off. They each are displayed by default.

AML Example:

    type:p2p_photo
    slug: <P2P photo slug>
    display_credit: <True/False> (optional)
    display_caption: <True/False> (optional)
    add_class: <css class> (optional)
    close_river: <True/False> (optional)

PHOTO ARRANGEMENTS
==================

*NEW FOR THIS ITERATION:* Running multiple photos in nicely designed configurations can enhance storytelling in wonderful ways. P2P photos are pulled from a P2P collection by the collection slug. There are several coniguration options, including a gallery, from which to choose. The options are identified by a number, and you might notice that design No. 2 requires only two photos. Only the first `n` photos will be displayed, with `n == design No.`. The exceptions are 0 and 1, which will display up to 100 photos, if you really need that many:

- 0: Formats as a touch-compatible gallery
- 1: A single stack of photos
- 2: two photos, side by side.
- 3: Three photos, the first fullwidth, the other two side-by-side underneath
- 4: A 2x2 grid of photos
- 5: Just like #2, except the first image is 75% width, the other is 25%.

AML Example:

    type: photo_arr
    slug: <P2P COLLECTION slug>
    design: <number from above list>
    display_credit: <True/False> (optional, for the photos)
    display_caption: <True/False> (optional, for the photos)
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


REFERS
======

There are several items worthy of <aside> refers, from subscription calls to action to project sidebars. The content for each refer is stored in the main spreadsheet's refers tab. Each refer requires a headline, text, button text and link url defined there. At present, the content options are:

    - methods
    - subscribe
    - press_release
    - appeals
    - assessor_response
    - study

AML Example: 

    type: refer
    content: <methods/subscribe>
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


ADVERTS
=======

We need some ads. Ugh.  They can be of type cube or billboard and can be full width (default) or notched right.

AML Example: 

    type: advert
    ad_type: <cube/billboard>
    ad_alignment: <full/right> (optional)
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


VIDEOS
======

This project highjacks the LAT video player because it is HTML5 and offers much better performance than the Flash-based embeds. The optional header property will insert a small label above the video.

Note: A previous iteration used a different method requiring different information. The HTML5 player just needs a P2P slug. 

AML Example: 

    type: video
    video_slug: <P2P video slug>
    header: <header text> (optional)
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


PULL QUOTES
===========

Pretty straightforward. Include desired quote marks inside the quote text. They are not added by this macro.

AML Example: 

    type: pullquote
    quote_text: "Lor tis blanditiis ducimus eum impedit nulla laboriosam!"
    quote_attribution: <Name name name>
    quote_attribution_secondary: <title or speaker description> (optional)
    add_class: <css class> (optional)
    close_river: <True/False> (optional)


ARBITRARY HTML
==============

Though unused in this project, just about anything can be dropped into the stories.

AML Example: 
    
    type: html
    content: <div>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deserunt culpa adipisci</div>
    :end
    close_river: <True/False> (optional)


HOW DO I ADD STORIES?
---------------------

As mentioned before, the content is organized by using a variable/label/part name. For isntance all content related to part 1 uses the keyword "assessments." This is how the story is pulled from the archieml. This is how the headlines, seo descriptions and other sundry items are pulled from the spreadsheet, and this is part of the story's url. It's also what creates a new batch of comments. Therefore, the first thing you should do is pick the part name. 

The name should be very representative to the content of the story. Next, copy the template from one of the existing stories and rename it `<part>.html`, where `<part>` is the name you just chose. 

Next, add the story text to the ArchieML. You can follow the patterns demonstrated in the previous stories for the various assets, but the first thing you will need is a header `[stories.<part>]` to create the new installment inside the ArchieML.

When you open up the template, you'll see a line that says `{% set part = "XXX" %}`. Set it to your chosen `<part>`. You'll also need to, for each new story, do these things:
    
    - Put properly-named video files and poster image into the img folder for the scrolling header.
    - Create, in the spreadsheet, entries for the poster image alt text and scrolling video caption/credits.
    - Create entries in the spreadsheet for headline, dek, og_descriptions (facebook, etc.), seo description, tweets and the desired social media thumbnail for the project (paste a tribimg.com url for the photo into the spreadsheet.) It would be good to look at the collection of text for previous stories to see what is needed.
    - Each of these items has corresponding entries on the story template. Be sure that the part name matches in each variable used.
    - Update the byline by using the `add_author()` macro. It takes the author's name and email address as arguments. Multiple authors should be seperated by commas.
    - Update the nav elements in the "navbar_elements" tab in the spreadsheet. This will populate both the sticky nav bar at the top and the larger box at the end of each story.
    - To reiterate, you don't need to do anything to pull in the story content besides loading it into the Google Doc (not spreadsheet) and setting the part variable.

Assumptions
-----------

* Python 2.7
* Tarbell 1.0.\*
* Node.js
* grunt-cli (See http://gruntjs.com/getting-started#installing-the-cli)
* Sass

Custom configuration
--------------------

## DEFAULT_CONTEXT['OMNITURE']

This project uses [python-tribune-omniture](https://github.com/newsapps/python-tribune-omniture) to render the Omniture `<script>` tags for the Tribune's analytics.  You'll need to configure the dictionary named `OMNITURE` in the `DEFAULT_CONTEXT` dictionary in your `tarbell_config.py`:


    DEFAULT_CONTEXT = {
        'name': 'lead',
        'title': 'Lead',
        'analytics_path': '',
        'OMNITURE': {
            'domain': 'chicagotribune.com',
            'sitename': 'Chicago Tribune',
            'section': 'news',
            'subsection': 'watchdog',
            'subsubsection': '',
            'type': 'dataproject',
        },
    }

Building front-end assets
-------------------------

This project uses [npm scripts](https://css-tricks.com/why-npm-scripts/) with a little help from [Grunt](http://gruntjs.com/) to build front-end assets.

To compile CSS and JavaScript for this project, first install the build tool depenencies:

    npm install

When you run:

    npm run build    

npm will compile `sass/styles.scss` into `css/styles.css` and bundle/minify `js/src/app.js` into `js/app.min.js`.

If you want to recompile as you develop, run:

    npm run build && npm run watch


The blueprint simply sets up the the build tools to generate `styles.css` and `js/app.min.js`, you'll have to explicitly update your templates to point to these generated files.  The reason for this is to make you think about whether you're actually going to use an external CSS or JavaScript file and avoid a request for an empty file if you don't end up putting anything in your custom stylesheet or JavaScript file.

To add `styles.css`, add this to your template file (likely, `index.html`):

    
    <link rel="stylesheet" href="css/styles.css">
    

To add `app.min.js` to your template file:

    
    <script src="js/app.min.js"></script>
    