var orig = null;

function isimage (url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}

function applyMarkup (markup) {
    // {{{!language, newline, code, !}}}
    var regex = new RegExp('\\{\\{\\{!([^\\n]*)\n((.|\\n)*)!\\}\\}\\}', 'm')
    $('p.desc').html(markup.replace(regex, '<pre class="sh_$1">$2</pre>'));

    sh_highlightDocument('/static/js/lang/', '.min.js');
}

function refreshMarkup() {
    applyMarkup($('#editdesc').val());
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

function openEdit(btn) {
    while (orig == null) {}

    $(btn).remove();
    $('#editdescform').show();
    $('#editdesc').val(orig);

    setInterval(refreshMarkup, 3000);
}

$(document).ready(function () {
    var desc = $('p.desc');
    orig = desc.html();
    applyMarkup(orig);
    loadMathJax();
});

// http://docs.mathjax.org/en/v1.1-latest/dynamic.html
function loadMathJax() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src  = "http://cdn.mathjax.org/mathjax/latest/MathJax.js";

  var config = 'MathJax.Hub.Config({' +
                 'extensions: ["tex2jax.js"],' +
                 'jax: ["input/TeX","output/HTML-CSS"]' +
               '});' +
               'MathJax.Hub.Startup.onload();';

  if (window.opera) {script.innerHTML = config}
               else {script.text = config}

  document.getElementsByTagName("head")[0].appendChild(script);
};
