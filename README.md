# rest-uploader
REST API File Uploader for Joplin

[API Reference](https://joplin.cozic.net/api/)

Joplin client will need Webclipper service enabled.
* Go to Tools -> Web Clipper Options -> Enable Web Clipper Service


### Tesseract
In order for OCR text recognition to work, you'll need to download and
install Tesseract. Windows systems may require that you add a path variable
in order for it to work.

### Poppler
Poppler is required for PDF processing.
For Windows, download x86 binary and add to environment path.
https://blog.alivate.com.au/poppler-windows/


### Running application
Launch using the executable rest_uploader, specify the monitoring path
as an argument. You'll need your Joplin API key the first time you
launch. If your API key changes or gets pasted incorrectly, delete the .api_token.txt file that gets stored to the package.

` rest_uploader /path/to/directory `

To launch as python module:

` python -m rest_uploader.cli /path/to/directory `
