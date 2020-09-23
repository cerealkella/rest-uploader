=======
History
=======

0.1.0 (2019-04-14)
------------------

* First super-unpolished and barely usable release on PyPI.


0.3.0 (2019-06-26)
------------------

* First real release on PyPI.


0.4.0 (2019-11-12)
------------------

* Fixed multipage OCR on PDFs
* Added Language as a command line option


0.5.0 (2019-11-14)
------------------

* Removed unidecode function on OCR, no longer needed


0.6.0 (2019-11-14)
------------------

* Cleaned up PDF reading function
* Syncronized versioning


0.7.0 (2019-11-14)
------------------

* Nothing of consequence


0.8.0 (2019-11-14)
------------------

* Added --version flag on cli


1.2.0 (2019-11-14)
------------------

* Resolved failed builds related to bumpversion and
  manual versioning out of sync


1.3.0 (2019-12-03)
------------------

* Added special processing to turn CSVs into markdown tables


1.4.0 (2020-02-19)
------------------

* Ignore .part files (KDE Bug)
* Added logic to automatically assign tags to newly created notes
* Added click option to turn off automatic tag generation


1.5.0 (2020-02-19)
------------------

* Embarrassingly dumb bug fix for autotag argument


1.7.0 (2020-05-11)
------------------

* Added command line options for server, port, destination notebook
* Added some error handling to quit when Joplin is closed or there
  is no valid notebook detected
* Removed the settings.py file - everything handled via command line
  switches
* More verbose command line notifications
* Not leaving temp file location setting to user, handling this by 
  detecting OS on startup


1.9.0 (2020-05-12)
------------------

* Immediately realized closing application if Joplin isn't running is
  a bad idea in the case of startup scripts, etc - fixed logic to wait
* Made use of the tempfile library which made life easier


1.10.0 (2020-05-12)
-------------------

* Fixed minor but annoying typo on a print statement


1.11.0 (2020-05-12)
-------------------

* Refactoring the imaging module out of rest_uploader and into its
  own img_processor module for reusability
* Added logic and command line switches (-r, -m) for autorotation and
  moving/"sweeping" files after uploading. Run rest-uploader --help
