// Convert .md links to .html in the generated HTML
// Safer implementation: operate on the original attribute value, and
// only modify same-origin or relative links.

// Using a for-loop avoids creating lots of temporary closures on old browsers
// and is easy to step through during debugging.
document.addEventListener('DOMContentLoaded', function() {
  var links = document.querySelectorAll('a[href]');
  for (var i = 0; i < links.length; i++) {
    var link = links[i];
    var href = link.getAttribute('href');
    if (!href) continue;

    // Skip obvious non-HTTP links and fragments
    if (href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0 || href.indexOf('javascript:') === 0 || href.indexOf('#') === 0) {
      continue;
    }

    // Resolve URL against the document base to detect same-origin absolute URLs.
    try {
      var resolved = new URL(href, document.baseURI);
      if (resolved.origin !== location.origin) continue; // skip external hosts
    } catch (e) {
      // If URL parsing fails, treat as a relative URL and continue
    }

    if (href.indexOf('.md') !== -1) {
      var newHref = href.replace(/\.md([\?#]|$)/g, '.html$1');
      link.setAttribute('href', newHref);
    }
  }
});
