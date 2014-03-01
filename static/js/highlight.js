$(document).ready(function () {
    console.log('ready');

    var desc = $('p.desc');
    // {{{!language, newline, code, !}}}
    var regex = new RegExp('\\{\\{\\{!([^\\n]*)\n((.|\\n)*)!\\}\\}\\}', 'm')

    console.log('{{{!lang\nblah blah\nline 3\ntest\n!}}}'.match(regex));
    desc.html(desc.html().replace(regex, '<pre class="sh_$1">$2</pre>'));

    sh_highlightDocument('/static/js/lang/', '.min.js');
})
