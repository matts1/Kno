var orig = null;

function isimage (url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}

function esc(val, orig, final) {
    return val.replace(new RegExp(orig, 'mg'), '&' + final + ';');
}

function remove(arr, item) {
    for(var i = arr.length; i--;) {
        if(arr[i] === item) {
            arr.splice(i, 1);
        }
    }
}

function applyMarkup (markup, refresh) {
    if (refresh) {
        markup = esc(esc(esc(esc(markup, '&', 'amp'), '<', 'lt'), '>', 'gt'), '"', 'quot');
    }
    markup += '\n';

    var regexes = [
        [  // newline, ```language, newline, code```, newline
            '\n```([^\\n]*)\n((.|\n)*?)```\n',
            '<pre class="sh_$1">$2</pre>'
        ],[  // ~~strikethrough~~
            '~~([^\n]*?)~~',
            '<del>$1</del>'
        ],[  // unordered list
            '(-\\S?([^\n]+)\n)+',
            function (match, capture) {
                match = match.split('\n');
                for (var i = 0; i < match.length; i++) {
                    match[i] = match[i].substring(2);
                }
                remove(match, '');
                return '<ul><li>' + match.join('</li><li>') + '</li></ul>';
            }
        ],[  // implements paragraph using 2 newlines
            '\\n[\n]+',
            '<br><br>'
        ],[  // implements newline using 1 newline
            '\\n',
            '<br>'
        ],[  // italics using a single underscore at the start or end of a word
            '\\b_([^\n]*?)_\\b',
            '<i>$1</i>'
        ],[  // bold using a single asteriks
            '\\*([^\n]*?)\\*',
            '<b>$1</b>'
        ]
    ];
    for (var i = 0; i < regexes.length; i++) {
        markup = markup.replace(new RegExp(regexes[i][0], 'mg'), regexes[i][1]);
    }

    $('p.desc').html(markup);

    $('p.desc pre.sh_io').each(function () {
        $(this).css('color', '#1546d7');
        $(this).css('font-weight', '700');
        $(this).html($(this).html().replace(
            new RegExp('&lt;&lt;&lt;(.*?)<br>', 'mg'),
            '<span style="color: black">$1</span><br>')
        );
    });

    sh_highlightDocument('/static/js/lang/', '.min.js');
}

function refreshMarkup() {
    applyMarkup($('#editdesc').val(), 1);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, 'description']);
}

function rp(val, orig, final) {
    return val.replace(new RegExp('&' + orig + ';', 'mg'), final);
}

function openEdit(btn) {
    while (orig == null) {}
    orig = rp(rp(rp(rp(orig, 'lt', '<'), 'gt', '>'), 'quot', '"'), 'amp', '&');
    $(btn).remove();
    $('#editdescform').show();
    $('#editdesc').val(orig);

    setInterval(refreshMarkup, 1000);
}

$(document).ready(function () {
    var desc = $('p.desc');
    orig = desc.html();
    applyMarkup(orig, 0);
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
