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
    "sec:org211dc5a"
    "sec:orgdbf23f6"
    "sec:org1b3e9ff"
    "sec:org0a7b42f"
    "sec:orge7749bf"
    "sec:org7dbc137"
    "sec:org73c2e53"
    "sec:org439d68d"
    "sec:org2909d33"
    "sec:orgdbb0adb"
    "sec:orge4022a3"
    "sec:orgfd2fa35"
    "sec:orgeadfc91"
    "sec:org4ba9ab8"
    "sec:orge1bf18c"
    "sec:org13cda33"
    "sec:org1687a99"
    "sec:orgbf2996e")
   (LaTeX-add-bibliographies
    "repport"))
 :latex)

