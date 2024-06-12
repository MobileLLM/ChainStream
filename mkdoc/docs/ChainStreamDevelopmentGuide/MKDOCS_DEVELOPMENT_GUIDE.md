# Project MkDocs Development Guide

This project uses mkdocs as the documentation framework and the Material for MkDocs theme.

Mkdocs can compile markdown files into html files and deploy them to github pages. Most of the website configuration has been completed, only the markdown files need to be written.

## Installation for MkDocs and Material for MkDocs

``` bash
pip install mkdocs
pip install mkdocs-material
pip install mike
pip install mkdocs-rss-plugin
pip install mkdocs-minify-plugin
pip install mkdocs-static-i18n
```

## Commands for MkDocs

``` bash
# Local preview, need to cd to mkdocs directory, will start a local server on port 8000
mkdocs serve

# Deployment, need to cd to mkdocs directory, will automatically deploy the latest documentation to the gh-pages branch of the github repo
mkdocs gh-deploy --force


mike deploy --push --update-aliases x.x latest
```

## Development Flow


!!! warning "notice branch"
    
    The documentation is mainly developed on the doc branch, please do not switch the branch to the wrong one.


1. Switch to the doc branch
2. cd to the ChainStream/mkdoc directory and run the `mkdocs serve` command to start a local server on port 8000
3. Write markdown files in the ChainStream/mkdoc/docs directory and save
4. If you add a new branch, you need to configure the nav configuration in the ChainStream/mkdoc/mkdocs.yml file
5. Save the changes, and then access http://localhost:8000/ to see the latest documentation
6. After confirming, commit the code to the doc branch and push it to the github repository
7. Use the `mkdocs gh-deploy` command to automatically deploy the latest documentation to the gh-pages branch of the github repository
8. Wait for a few minutes, and then you can see the latest documentation in https://chainstream.github.io/ChainStream/

## Support for Double Language

This project uses the mkdocs-static-i18n plugin to support double-language.

Specifically, this project has been configured with two languages, English and Chinese, and the default language is Chinese. The default configuration in the mkdocs.yml file uses the English configuration. If you want to support Chinese, you need to construct a markdown file with the same name but with a .zh.md suffix.

Additionally, in the mkdocs.yml file, the nav_translations: option is used to implement navigation bar translations for different languages.


## Reference

!!! note "Reference"
    Although the following document is longer, over 90% of the questions can be found in the links below.

- [https://www.mkdocs.org/](https://www.mkdocs.org/)
- [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- [http://www.cuishuaiwen.com:8000/zh/PROJECT/TECH-BLOG/mkdocs_and_material/#material_3](http://www.cuishuaiwen.com:8000/zh/PROJECT/TECH-BLOG/mkdocs_and_material/#material_3)