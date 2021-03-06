/*
 * Annotation configuration settings
 * These differ between the Moodle and stand-alone versions
 */

ANNOTATION_LINKING = true;		// If true, include the linking feature
ANNOTATION_KEYWORDS = true;	// If true, include the keywords feature
ANNOTATION_ACCESS = true;		// If true, include the public/private feature
ANNOTATION_EXTERNAL_LINKING = true;	// If true, link editor accepts any http/https URL

ANNOTATION_ACCESS_DEFAULT = 'private';	// default access

// If this is true, uses paths like annotate/nnn
// if false, use paths like annotation/annotate.php?id=nnn
ANNOTATION_NICE_URLS = true;

NICE_ANNOTATION_SERVICE_URL = '/annotate';
UGLY_ANNOTATION_SERVICE_URL = '/annotate';

/* Logging Settings */
TRACING_ON = true;		// switch on to output trace() calls
LOGGING_ON = true;		// switch on to output logError() calls
INWINDOW_LOG = false;	// switch on to output to HTML document instead of/in addition to console

// Set these to true to view certain kinds of events
// Most of these are only useful for debugging specific areas of code.
// annotation-service, however, is particularly useful for most debugging
setTrace( 'annotation-service', true );	// XMLHttp calls to the annotation service
setTrace( 'word-range', false );			// Word Range calculations (e.g. converting from Text Range)
setTrace( 'find-quote', false );			// Check if quote matches current state of document
setTrace( 'node-walk', false );			// Used for going through nodes in document order
setTrace( 'show-highlight', false );		// Text highlighting calculations
setTrace( 'align-notes', false );			// Aligning margin notes with highlighting
setTrace( 'range-compare', false );		// Compare range positions
setTrace( 'range-string', false );			// Show conversions of word ranges to/from string
setTrace( 'list-annotations-xml', false );// Show the full Atom XML coming back from listAnnotations
setTrace( 'WordPointWalker', false );		// Show return values from WordPointWalker
setTrace( 'prefs', false );				// List fetched preferences
setTrace( 'keywords', false );				// List fetched keywords
setTrace( 'point-compare', false );			// Compare two WordPoints
