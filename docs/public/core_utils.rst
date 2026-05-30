Core utils
==========

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: Full API

    ../../core_utils/core_utils.api.rst

Core utils package contains auxiliary materials to help you implement
your laboratory works. We are going to over each of its parts
to guide you when and how to use it.

Article package
---------------

The ``article`` package is responsible for handling the articles you
have collected from your website. You are going to use it for both
Lab 5 and Lab 6. See exhaustive guide for :ref:`ctlr-article-label`.

Configurations DTO
------------------

The ``config_dto.py`` module defines a :py:class:`core_utils.config_dto.ConfigDTO` abstraction.
This abstraction is responsible for indicating what fields must be passed as
a configuration settings along with what their types must be.

They match the fields of the ``scraper_config.json`` configuration file.
For more details on what each of the parameters presents, refer to :ref:`scraper-label`.

.. note:: During implementation of Lab 5, make sure to return
          a ``ConfigDTO`` instance from the
          :py:func:`lab_5_scraper.scraper.Config._extract_config_content` method.

Module with constants
---------------------

``constants.py`` module defines the following constant values:

-  ``PROJECT_ROOT``: a path to ``2025-2-level-ctlr`` folder,
   which the root of the current project;
-  ``ASSETS_PATH``: a path to ``2025-2-level-ctlr/tmp/article`` folder,
   where all the collected articles must be stored;
-  ``CRAWLER_CONFIG_PATH``: a path to ``lab_5_scraper/scraper_config.json``
   file with configuration parameters for scraper;
-  ``PROJECT_CONFIG_PATH``: a path to ``2025-2-level-ctlr`` folder
   configuration file (*this is an admin utils related item and
   is not intended for you to interact with it*);
-  ``NUM_ARTICLES_UPPER_LIMIT``: a maximum number for articles to be
   collected, anything above this number must be considered invalid;
-  ``TIMEOUT_LOWER_LIMIT``: a minimum number of seconds for a timeout,
   anything below this number must be considered invalid;
-  ``TIMEOUT_UPPER_LIMIT``: a maximum number of seconds for a timeout,
   anything above this number must be considered invalid.

.. attention:: Can you tell why the folder for articles is located in the
               directory with the name ``tmp``?

.. note:: Make sure to import these constants from the ``constants.py`` module
          and use them whenever you need to specify a path or boundary values
          (for example, when validating configuration values).

Pipeline module
---------------

The ``pipeline.py`` module defines the supporting abstractions for working on Lab 6.
You may notice that most of the abstractions are protocols.
The **protocol** is a set of methods or attributes that an object must have
in order to be considered compatible with that protocol.
It influences the code implicitly and, if necessary, organizes a check
for the presence of methods or attributes in the corresponding classes.

:py:class:`core_utils.pipeline.LibraryWrapper` defines a specific set of methods and attributes
to be present across all model wrappers:

-  ``_analyzer`` attribute
-  ``_bootstrap`` method
-  ``analyze`` method
-  ``to_conllu`` method

:py:class:`core_utils.pipeline.PipelineProtocol` defines an interface for pipelines:
they must have a ``run`` method.

Dataclass :py:class:`core_utils.pipeline.TreeNode` stores information about
the node of syntactic tree:

-  POS tag
-  text
-  dependent children

Visualizer module
-----------------

As one of the tasks for mark 8 you are expected to perform an
analysis of distribution of part-of-speech tags in the processed
collected articles. This is where ``visualizer.py`` module comes into play.
Its :py:func:`core_utils.visualizer.visualize` function takes an
``Article`` instance along with a path and creates a bar chart depicting
POS distribution in the specified location.

.. note:: :py:func:`core_utils.visualizer.visualize` function must be called
          during the execution of
          :py:meth:`lab_6_pipeline.pipeline.POSFrequencyPipeline.run` method,
          but before that, make sure you have already filled the
          ``pos_frequencies`` field of the corresponding meta file.

.. note:: The name of the resulting image must have the same id as
          the article analysed.

Tests package
-------------

To make sure that the provided materials work as intended, they are
thoroughly tested. The ``tests`` package
contains a number of unit-tests for ``article`` package,
``config_dto.py`` module, and ``visualizer.py`` module.

During work on Lab 5 and Lab 6, you do not need to
interact with these tests. However, you should suspect that the provided
modules behave unexpectedly, examination of these tests may help catch
the bug. Any suggestion on improvements of core utils is encouraged and
rewarded.
