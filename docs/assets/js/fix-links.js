// Convert .md links to .html in the generated HTML
document.addEventListener('DOMContentLoaded', function() {
  // Fix all navigation links
  document.querySelectorAll('a[href]').forEach(function(link) {
    // Only convert markdown links to HTML
    if (link.href.includes('.md')) {
      link.href = link.href.replace(/\.md([\?#]|$)/g, '.html$1');
    }
  });
});
