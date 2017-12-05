(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("fncychap" "Bjornstrup") ("xcolor" "dvipsnames") ("babel" "french" "english")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "minted"
    "pdflscape"
    "fncychap"
    "xcolor"
    "babel")
   (LaTeX-add-labels
    "sec:orgb15ca06"
    "sec:orge690953"
    "sec:orgaef469d"
    "sec:org41aca82"
    "sec:org52f447f"
    "sec:org1a1aff5"
    "sec:org31a4e3a"
    "sec:orgc1b8eee"
    "sec:orgaa36967"
    "sec:orgfd833c7"
    "sec:orgbae05e7"
    "sec:org9877354"
    "sec:org2e16211"
    "sec:org05d8e83"
    "sec:org401bc18"
    "sec:org809a764"
    "sec:org926b49b"
    "sec:org740b4c0"
    "sec:org02e1c9f"
    "sec:orgd9edb86"
    "sec:orgd637277"
    "sec:org491925f"
    "sec:orga9a1dc4"
    "sec:org80f8f36"
    "sec:orgd30715e"
    "sec:org3df8ade"
    "sec:orge10d028"
    "sec:org11bccae"
    "sec:org4ffee0c"
    "sec:orgc942394"
    "sec:orgbacaea0"
    "sec:orge5d03b4"
    "sec:org0dfd64f"
    "sec:orgac2562d"
    "sec:orgc690ceb"
    "sec:org7bd1ab0"
    "sec:orgf51b797"
    "sec:org6c93fce"
    "sec:org3a80c39")
   (LaTeX-add-bibliographies
    "repport"))
 :latex)

