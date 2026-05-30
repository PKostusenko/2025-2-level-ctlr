Technical Track of Computer Tools for Linguistic Research (2025/2026)
=====================================================================

As a part of a compulsory course `Computer Tools for Linguistic
Research <https://nnov.hse.ru/ba/ling/courses/1128051801.html>`__ in `National
Research University Higher School of Economics <https://www.hse.ru/>`__.

This technical track is aimed at building basic skills for retrieving
data from external WWW resources and processing it for future linguistic
research. The idea is to automatically obtain a dataset that has a
certain structure and appropriate content, perform morphological
analysis using various natural language processing (NLP) libraries.
Dataset requirements :ref:`dataset-label`.


Instructors:
------------

-  `Klimova Margarita Andreevna <https://www.hse.ru/org/persons/91748436>`__ -
   linguistic track lecturer
-  `Lyashevskaya Olga Nikolaevna <https://www.hse.ru/staff/olesar>`__ -
   linguistic track lecturer
-  `Demidovskij Alexander
   Vladimirovich <https://www.hse.ru/staff/demidovs#sci>`__ - technical
   track lecturer
-  `Uraev Dmitry Yurievich <https://www.hse.ru/org/persons/208529395>`__ -
   technical track practice lecturer
-  `Zharikov Egor Igorevich <https://t.me/godb0i>`__ - technical track expert


-  `Nurtdinova Sofia Alekseevna <https://t.me/sunrielly>`__ - technical track assistant
-  `Podpryatova Anna Sergeevna <https://t.me/anpruch>`__ - technical track assistant
-  `Klimov Andrey Petrovich <https://t.me/hollow_shelves_quiet_hell>`__ -
   technical track assistant
-  `Evgrafova Anna Sergeevna <https://t.me/evgraff_19>`__ - technical track assistant


Project Timeline
----------------

1. **Scraper**:

   1. Short summary: Your code can automatically parse a media website
      you are going to choose, save texts and its metadata in a proper
      format.
   2. Deadline: **May, 11**.
   3. Format: each student works in their own PR.
   4. Dataset volume: 100 articles.
   5. Design document: :ref:`scraper-label`.

2. **Pipeline**:

   1. Short summary: Your code can automatically process raw texts from
      previous step, make point-of-speech tagging and basic
      morphological analysis.
   2. Deadline: **June, 1**.
   3. Format: each student works in their own PR.
   4. Dataset volume: 100 articles.
   5. Design document: :ref:`pipeline-label`.


Lectures history
----------------

+------------+---------------------+--------------------------------------------------------------+
| Date       | Lecture topic       | Important links                                              |
+============+=====================+==============================================================+
| 06.04.2026 | Lecture:            | N/A                                                          |
|            | Introduction to     |                                                              |
|            | technical track.    |                                                              |
|            | 3rd party libraries.|                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 13.04.2026 | Lecture:            | `Листинг <./seminars/seminar_04_13_2026/try_requests.py>`__. |
|            | Headers. HTML       |                                                              |
|            | structure.          |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 13.04.2026 | Seminar: Local      | N/A                                                          |
|            | setup. Choose       |                                                              |
|            | website.            |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 20.04.2026 | Lecture: Search in  | `Листинг <./seminars/seminar_04_20_2026/try_bs.py>`__.       |
|            | HTML page.          |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 20.04.2026 | Seminar: `requests`:| N/A                                                          |
|            | install, API.       |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 27.04.2026 | Lecture: Filesystem | `Листинг <./seminars/seminar_04_27_2026/try_paths.py>`__.    |
|            | with `pathlib`.     |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 27.04.2026 | Seminar: `datetime`,| `Листинг <./seminars/seminar_04_27_2026/try_dates.py>`__.    |
|            | `json`, `pathlib`.  | `Листинг <./seminars/seminar_04_27_2026/try_json.py>`__.     |
+------------+---------------------+--------------------------------------------------------------+
| 04.05.2026 | Holidays.           | N/A                                                          |
+------------+---------------------+--------------------------------------------------------------+
| 11.05.2026 | Seminar: Lab 5      | N/A                                                          |
|            | handover.           |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 18.05.2026 | Seminar: text       | `Листинг <./seminars/seminar_05_18_2026/try_udpipe.py>`__.   |
|            | analysis with       |                                                              |
|            | `udpipe`.           |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 25.05.2026 | Seminar: graph      | `Листинг <./seminars/seminar_05_25_2026/try_networkx.py>`__. |
|            | analysis with       |                                                              |
|            | `networkx`.         |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 01.06.2026 | Seminar: Lab 6      | N/A                                                          |
|            | handover.           |                                                              |
+------------+---------------------+--------------------------------------------------------------+
| 08.06.2026 | Seminar: Extra      | N/A                                                          |
|            | handover day (with  |                                                              |
|            | penalties).         |                                                              |
+------------+---------------------+--------------------------------------------------------------+


You can find a more complete summary from lectures in :ref:`ctlr-lectures-label`.

Technical solution
------------------

+-----------------------+---------------------------+--------------+---------+
| Module                | Description               | Component    | Need to |
|                       |                           |              | get     |
+=======================+===========================+==============+=========+
| `pathlib              | working with file paths   | scraper      | 4       |
| <https://pypi.org     |                           |              |         |
| /project/pathlib/>`__ |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `requests <https://   | downloading web pages     | scraper      | 4       |
| pypi.org/project/reque|                           |              |         |
| sts/2.25.1/>`__       |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `BeautifulSoup4       | finding information on    | scraper      | 4       |
| <https://pypi.org     | web pages                 |              |         |
| /project/beautifulso  |                           |              |         |
| up4/4.11.1/>`__       |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `lxml <https://pypi.  | **optional** parsing HTML | scraper      | 6       |
| org/project/lxml/>`__ |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| ``datetime``          | working with dates        | scraper      | 6       |
+-----------------------+---------------------------+--------------+---------+
| ``json``              | working with json text    | scraper,     | 4       |
|                       | format                    | pipeline     |         |
+-----------------------+---------------------------+--------------+---------+
| `spacy_udpipe <https: | module for morphological  | pipeline     | 6       |
| //pypi.org/project    | analysis                  |              |         |
| /spacy-udpipe/>`__    |                           |              |         |
+-----------------------+---------------------------+--------------+---------+
| `networkx <https:/    | working with graphs       | pipeline     | 10      |
| /pypi.org/project     |                           |              |         |
| /networkx/>`__        |                           |              |         |
+-----------------------+---------------------------+--------------+---------+

Software solution is built on top of three components:

1. `scraper.py <https://github.com/fipl-hse/2025-2-level-ctlr/blob/main/lab_5_scraper/scraper.py>`__
   - a module for finding articles from the given media, extracting text and dumping it to
   the file system. Students need to implement it.
2. `pipeline.py <https://github.com/fipl-hse/2025-2-level-ctlr/blob/main/lab_6_pipeline/pipeline.py>`__
   - a module for processing text: point-of-speech tagging and basic
   morphological analysis. Students need to implement it.
3. `article.py <https://github.com/fipl-hse/2025-2-level-ctlr/blob/main/core_utils/article/article.py>`__
   - a module for article abstraction to encapsulate low-level manipulations with the article.


Resources
---------

1. `Academic performance <https://docs.google.com/spreadsheets/d/1wCyGfGEXwjnB0p8WMbSCMJlmpxeQfG07QMGDnfiYFhI/>`__
2. `Media websites list <https://docs.google.com/spreadsheets/d/1rKtvIpzmUFmXL5NVUEVfsmuLc4AWhzmOOQ0xPgBulsI/edit?gid=0#gid=0>`__
3. `Python programming course from previous semester
   <https://github.com/fipl-hse/2025-2-level-labs>`__
4. `Scraping tutorials (Russian) <https://youtu.be/7hn1_t2ZtJQ>`__
5. `Scraping tutorials (English)
   <https://www.youtube.com/playlist?list=PL1jK3K11NINiOn4DdIDVdyQpcU3kaNxl0>`__
6. `Useful documentation <https://fipl-hse.github.io/docs/useful_docs/ctlr_docs/index.html>`__
