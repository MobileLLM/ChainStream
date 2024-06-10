# 项目文档开发指南

本项目使用 mkdocs 作为文档框架，使用 Material for MkDocs 主题。

该框架可以直接将markdown文件编译成html文件，并部署到github pages上。目前已经完成了大部分网页配置，只需要编写markdown文件即可。

## 本地开发环境搭建

``` bash
pip install mkdocs
pip install mkdocs-material
pip install mike
pip install mkdocs-rss-plugin
pip install mkdocs-minify-plugin
pip install mkdocs-static-i18n
```

## 开发命令

``` bash
# 本地预览， 需要cd到mkdocs目录下， 会在本地启动一个服务，默认端口为8000
mkdocs serve

# 自动部署， 需要cd到mkdocs目录下， 会自动将最新文档部署到github repo的gh-pages分支
mkdocs gh-deploy --force


mike deploy --push --update-aliases x.x latest
```

## 双语支持

本项目使用 mkdocs-static-i18n 插件实现了双语支持。

具体来说，本项目配置了en和zh两种语言，默认支持zh语言。在mkdocs.yml文件中的nav配置中默认使用en配置。若想支持zh语言，则需要构造同名但以.zh.md结尾的markdown文件。

同时，在mkdocs.yml文件中配置nav_translations:选项以实现不同语言的导航栏翻译。


## Reference

!!! note "参考文档"
    虽然下面文档较长，但超过90%的问题都可以从下面的链接中找到答案。

- [https://www.mkdocs.org/](https://www.mkdocs.org/)
- [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
- [http://www.cuishuaiwen.com:8000/zh/PROJECT/TECH-BLOG/mkdocs_and_material/#material_3](http://www.cuishuaiwen.com:8000/zh/PROJECT/TECH-BLOG/mkdocs_and_material/#material_3)