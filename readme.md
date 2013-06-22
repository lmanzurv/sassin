
# INDENTEDSASS

This is a indented-SASS to CSS compiler. Indented-SASS is a  beautiful space-indented format to express CSS stylesheets.

It is a fork of the RapydCSS progject (https://bitbucket.org/pyjeon/rapydcss) to provide a smoother API for other pojects.

# What is SASS?

Okay this gets confusing. There is a Ruby program called SASS which used to compile a nice indented syntax for stylesheets into CSS. Let's call this the indented-SASS format. 

Indented-SASS used to be known as the SASS format, but SASS, the program, found that it was losing market share to LESS (another CSS extension format), and created the SCSS format. So SASS decided to deprecate the original indented-SASS format, and focus on the SCSS format. So now you have the case where SASS can compile indneted-SASS but would rather you compile SCSS. 

But indented-SASS is a lovely format that fits well with other space-indented, formats such as YAML and HAML, and of course, Python. However, if you want to use indented-SASS in Python, it gets complicated. 

The good news is that quite a few native Python libraries have been written that can compile SCSS into CSS (PySCSS, libsass, SASS). The bad news is that none of these modules actually recognize the indented-SASS format.

Anyway, I finally found a great little module RapydCSS that carries out this conversion. However, as the API is locked into the RapydScript project, I've forked it so that it behaves better with other projects.

## Installation

    pip install indentedsass

This installs the python module `indentedsass` in the standard default lbiraries. 

As well an executable script is installed:

   sass2css sass [optional_output]

## Indented-SASS format

### Flat mode.





