(TeX-add-style-hook
 "precomands"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("titlesec" "explicit")))
   (TeX-run-style-hooks
    "tikz"
    "kpfonts"
    "titlesec")
   (TeX-add-symbols
    "chapterlabel"))
 :latex)

