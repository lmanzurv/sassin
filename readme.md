
# inSASS

`inSASS` compiles the indented-SASS-syntax format, a beautiful space-indented format used to express CSS stylesheets. This format is similar to the Javascript-based [Stylus](http://learnboost.github.io/stylus/) format, but `inSASS` works entirely in the Python ecosystem.

_This is a fork of [RapydCSS](https://bitbucket.org/pyjeon/rapydcss)._

## Installation

    pip install indentedsass

This has one dependency `PySCSS` which should be automatically installed by pip. As well an executable script is installed:

    sass2css sass [css]


## What is inSASS?

Okay this gets confusing: there is a Ruby program called [SASS](http://sass-lang.com/) which used to compile an indented syntax for stylesheets into CSS, known as the original SASS format. However, SASS (the program) found that it was losing market share to LESS, and thus, introduced the SCSS format, which has a curly braced syntax to appear more like LESS. So SASS (the program) decided to deprecate SASS (the syntax) and focus on SCSS (the format). That's why, given this confusion, we use `inSASS` to describe the original indented-syntax format of SASS.

However, `inSASS` is a lovely format that fits well with other space-indented formats, such as YAML, HAML, and of course, Python. The good news is that there are a few Python SCSS libraries (PySCSS, libsass, SASS). The bad news is that none of these modules can actually compile the `inSASS` format, even though confusingly some of these libraries also use SASS in their name.

Happily, I found RapydCSS, a handy little `inSASS` compiler in Python. Because RapydCSS has a rather idiosyncratic API, I forked it to make some changes that help `inSASS` work better with other Python projects, such as HAMLPY.

## inSASS syntax in flat mode

`inSASS` tries to follow the [original indented syntax](http://sass-lang.com/docs/yardoc/file.INDENTED_SYNTAX.html) of SASS. 

The compilation provided by `inSASS` is straightforward: it wraps indented spaces with curly braces; and adds semicolons at the end of fields. This is sufficient to turn `inSASS` into valid SCSS, and thus future-proofs `inSASS` from deprecation in the SASS/SCSS world.

If your `inSASS` file does not use any of the bells and whistles below (variables, mixins, nesting, etc.), then this simple compilation step will give you valid CSS.

    import indentedsass

    s = '''
    body
      width: 500px
    '''

    print indentedsass.compile(s)

### Line extensions

Lines ending with `,` will be continued to the next line:

    #container, #article_container, #sidebar_container,
    #footer_container, #useless_container
      background-color: #DDD

That first line is treated is one whole line:

    #container, #article_container, #sidebar_container #footer_container, #useless_container {
      background-color: #DDD; }

### Comments

Comments are prefaced with `/*` and is implemented on a per-line basis:

    /* This is a comment
    /* This is another comment
    body
      /* Yep, a short width
      width: 50px 

Will give:

    /* This is a comment */
    /* This is another comment */
    body {
      /* Yep, a short width */
      width: 50px; }

## Syntax extensions of inSASS requiring PySCSS

But of course you want to take advantage of the programmatic syntax extensions introduced by SASS. This will require that you pre-install the `PySCSS` module, and the compilation is then:

    import indentedsass

    s = '''
    @mixin box($width)
      width: $width px
    body
      @include box(500)
    '''

    print indentedsass.compile_with_scss(s)

### Variable substitution

You can use variables, prefaced by a `$`:

    $highlight-color: #999
    #big-box
      border: 1px solid $highlight-color
    #message
      color: $highlight-color 

Which makes it much easier to pass colors around, as in the resultant CSS: 

    #big-box {
      border: 1px solid #999999;
    }
    #message {
      color: #999999;
    }

### Expressions

Cobble together simple expressions:

    $big-width: 500
    #container
      width: $big-width px
    $panel-left
      float: left
      width: $big-width/2 px

And we get, in the CSS:

    #container {
      width: 500 px;
    }
    $panel-left {
      float: left;
      width: 250 px;
    }

### Mix-ins with arguments

Mix-ins that group common elements, and can take arguments, which are prefaced by '@':

    @mixin left($dist)
      float: left
      margin-left: -$dist
      width: $dist - 20
      padding-right: 20

    #sidebar
      @include left(200px) 

Gives:

    #sidebar {
      float: left;
      margin-left: -200px;
      width: 180px;
      padding-right: 20;
    }

### Nesting

Handy nesting, and self reference `&` to save even more typing:

    #article
      a
        font:
          family: Garamond
        &:link
          text-decoration: none
        &:hover
          text-decoration: underline

Flattens out into:

    #article a {
      font-family: Garamond;
    }
    #article a:link {
      text-decoration: none;
    }
    #article a:hover {
      text-decoration: underline;
    }

### Class Extensions

Extend a class with a new twist:

    #message
      border: 1px solid red

    #bad-message
      @extend #message
      background-color: red

Creates a similar class quite easily:

    #bad-message, #message {
      border: 1px solid #ff0000;
    }
    #bad-message {
      background-color: #ff0000;
    }


Imports to be implemented




