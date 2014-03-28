.. Firapria documentation master file, created by
   sphinx-quickstart on Fri Mar 28 23:02:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Firapria's documentation!
====================================

.. toctree::
   :maxdepth: 2

Firapria is a lightweight library to get pollution indices for Paris, France.
It fetches its data from Airparif_, and thus provides you with yesterday’s,
today’s and tomorrow’s indices when it can. I developped it for a personal
project and thought it might be useful to others, so I wrapped it in a lib,
wrote tests and documentation, and here we are!

.. _Airparif: http://www.airparif.asso.fr/

Installation
------------

Install Firapria with ``pip``: ::

    [sudo] pip install firapria

It supports both Python 2.x and 3.x.

Usage
-----

The ``pollution`` module provides only one function for now: ::

    from firapria.pollution import get_indices

    indices = get_indices()

Note: due to the way Airparif generates its data, you’ll get only two indices
(for yesterday and today) if you use the function before 11 AM.

Indices types
~~~~~~~~~~~~~

Airparif gives its indices in two flavors: French and European ones. Firapria
gets European indices by default, but you can choose between both. ::

    from firapria import pollution as p

    fr_indices = p.get_indices(p.FR)  # e.g. [6, 7, 6]
    eu_indices = p.get_indices(p.EU)  # e.g. [64, 80, 65]

Caveats
-------

Because Airparif doesn’t have any public API, Firapria fetch and parse its
website. Indices are not often updated during the day, so you should cache
results to preserve Airparif’s bandwidth.
