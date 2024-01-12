function onOpen() {
  var ui = DocumentApp.getUi();
  ui.createMenu('Latex Tools')
      .addItem('Insert Latex Images', 'insertLatexImages')
      .addToUi();
}

function insertLatexImages() {
  var doc = DocumentApp.getActiveDocument();
  var body = doc.getBody();
  var paragraphs = body.getParagraphs();
  
  // Mapping of heading indices to folder names
  const headingFolderMap = {
    "1": "1_home",
    "2": "2_airfoil_latex",
    "3": "3_wing_latex",
    "4": "4_drag_incompressible_latex",
    "5": "5_drag_compressibility_latex",
  };

  Logger.log("Starting to process the document.");

  var i = 0;
  while (i < paragraphs.length) {
    var paragraph = paragraphs[i];

    // Check if the paragraph is a Heading 2
    if (paragraph.getHeading() === DocumentApp.ParagraphHeading.HEADING2) {
      var headingText = paragraph.getText();
      var headingIndex = headingText.split('.')[0].trim();
      var folderName = headingFolderMap[headingIndex];

      if (folderName) {
        Logger.log("Processing folder: " + folderName);
        var imagesInserted = insertImagesFromFolder(body, i + 1, folderName);
        i += imagesInserted * 2 + 1; // Move to the next paragraph after the last inserted image
      } else {
        Logger.log("No mapping found for heading: " + headingText);
        i++;
      }
    } else {
      i++;
    }

    // Refresh the paragraphs list to get the updated structure
    paragraphs = body.getParagraphs();
  }

  Logger.log("Document processing complete.");
}


function insertImagesFromFolder(body, paragraphIndex, folderName) {
  var parentFolder = DriveApp.getFoldersByName("latex_renders").next();
  var targetFolder = parentFolder.getFoldersByName(folderName).next();
  var files = targetFolder.getFiles();

  var images = [];
  while (files.hasNext()) {
    var file = files.next();
    if (file.getMimeType().indexOf('image') !== -1) {
      images.push(file);
    }
  }

  // Sort the images by name
  images.sort(function(a, b) {
    return a.getName().localeCompare(b.getName());
  });

  images.forEach(function(file) {
    Logger.log("Inserting image: " + file.getName());
    var image = file.getBlob();
    var newParagraph = body.insertParagraph(paragraphIndex, '');
    newParagraph.appendInlineImage(image);

    // Insert an empty paragraph after the image
    body.insertParagraph(paragraphIndex + 1, '');
    paragraphIndex += 2;
  });

  return images.length;
}
