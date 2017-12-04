(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("fncychap" "Bjornstrup") ("xcolor" "dvipsnames") ("babel" "french" "english")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
<<<<<<< HEAD
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
=======
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
>>>>>>> f382704981da7791e942c2af2549e7a5442f0f3a
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
<<<<<<< HEAD
    "sec:orgebfc6ba"
    "sec:orgf364af3"
    "sec:org862efb2"
    "sec:orge2fcf92"
    "sec:org8def52d"
    "sec:org3c2956d"
    "sec:org695c8de"
    "sec:org6378ae7"
    "sec:org4dad2ca"
    "sec:org63e069b"
    "sec:org1bcc857"
    "sec:org01b5e31"
    "sec:org1cdc3ec"
    "sec:org77a3c8a"
    "sec:org7ac2bb7"
    "sec:orgb7a574c"
    "sec:org35aa644"
    "sec:org0e3ec6c"
    "sec:org32f6cc6"
    "sec:org758a55c"
    "sec:orged8ffb8"
    "sec:org44da44a"
    "sec:orgcfdbfb0"
    "sec:orgd953681"
    "sec:orge615123"
    "sec:org636ea88"
    "sec:orgddb44db"
    "sec:org7dc963d"
    "sec:orgf39d758"
    "sec:orgf08b747"
    "sec:orgae7885b"
    "sec:orgda4b9b0"
    "sec:org67a507e"
    "sec:org035184d"
    "sec:org0fb3364")
=======
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
>>>>>>> f382704981da7791e942c2af2549e7a5442f0f3a
   (LaTeX-add-bibliographies
    "repport"))
 :latex)

