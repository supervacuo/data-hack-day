data-hack-day README
==============================

Carl van Tonder <carl@supervacuo.com>

Overview
----------------------------------

``data-hack-day`` is a `Django`_ application\ [#resuable]_ to visualise social
media data, developed during the `OccupyData Hackfest NYC`_, March 23-24
2012. It currently handles YouTube videos (using the `python-gdata YouTube API`_\ )
and manually-entered or CSV-uploaded online news articles, and draws a timeline
using `d3.js`_.

Installing
----------------------------------

Install on GNU/Linux using::

  git clone https://github.com/supervacuo/data-hack-day.git data-hack-day
  cd data-hack-day
  pip install -r reqirements.txt
  cp youtubeparty/local_settings.py{.example,}
  python manage.py syncdb
  python manage.py migrate
  python manage.py runserver

Features
----------------------------------

* Automatically import some metadata from YouTube videos and their comments by
  pasting in the video ID, thanks to the `python-gdata YouTube API`_.
* Create "Media objects" corresponding to online news stories, either by manual
  entry or CSV upload.
* Manage (edit and delete) "Media objects".
* Bugs and incompleteness (see below)

To-do
----------------------------------

* Find a better name for the project...
* New hierarchical layout for `d3.js`_, and navigation.
* Show tweets on the timeline visualisation.
* Work out the best way for users to bulk-import Twitter data.
* Use Topsy.com API more cleverly; deal with paginated responses and large
  result sets.
* Implement proper user profile and registration system.
* Date picker widget (tried; failed due to `Django bug`_).
* CSV upload error handling and documentation.
* Non-stupid tree implementation using `django-mptt`_.
* Tests.
* Clean up code, complete transition to class-based views, implement
  `django-guardian`_ carefully in all relevant views.
* *etc.* *etc.*
* Fix known bugs (see below).

Bugs
----------------------------------

Oh yes there are.

* No security system to speak of. (Don't deploy this on the open internet. I
  didn't...)
* Rendering strangeness. I still haven't completely got the hang of Twitter's
  `bootstrap`_ framework, so some things look slightly off.

Licence
----------------------------------

As many rights reserved as possible until I can work out which copyleft licence
I *can* release this under (hopefully AGPL).

Contributing
----------------------------------

HELP!

All patches, ideas gratefully accepted. Fork me (above), Github issues (also
above) or e-mail (above; slightly lower down), please.

.. [#resuable] It's not reusable yet, sorry...

.. _Django: http://djangoproject.com
.. _python-gdata YouTube API: https://developers.google.com/youtube/1.0/developers_guide_python
.. _SIMILE Timeline widget: http://www.simile-widgets.org/timeline/
.. _OccupyData Hackfest NYC: http://occupydatanyc.wordpress.com/
.. _d3.js: http://mbostock.github.com/d3/
.. _django-mptt: https://github.com/django-mptt/django-mptt
.. _django-guardian: https://github.com/lukaszb/django-guardian
.. _bootstrap: http://twitter.github.com/bootstrap/
.. _Django bug: https://code.djangoproject.com/ticket/17981
