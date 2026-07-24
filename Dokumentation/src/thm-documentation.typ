#let thm-green = rgb(128, 186, 36)
#let thm-gray = rgb(74, 91, 102)
#let thm-red = rgb(156, 19, 46)
#let thm-yellow = rgb(244, 170, 0)
#let thm-lightblue = rgb(0, 184, 228)
#let thm-blue = rgb(0, 40, 120)

#let documentation(
  module: "",
  term: "",
  title: "",
  authors: (),
  doc,
) = {
  set page(
    paper: "a4",
    margin: (top: 2cm, bottom: 3cm, x: 2cm),
  )
  set text(
    lang: "de",
    font: "Source Serif 4",
    size: 10pt,
  )
  set par(
    justify: true,
  )

  // Content
  set page(
    footer: [
      #text(font: "Source Sans 3", thm-gray, [
        #text(weight: "bold", module) | #term
        #h(1fr)
        #context [ #counter(page).display("1 / 1", both: true) ]
      ])
    ],
  )
  set heading(numbering: "1.")

  [
    #set align(center)
    #text(18pt, weight: "bold")[ #title ]

    #let index = 0
    #for author in authors {
      author.name
      footnote(numbering: "*", "Matrikelnummer: " + author.id)
      if (index < authors.len() - 1) [#if (index < authors.len() - 2) [, ] else [ und ]] else []
      index = index + 1
    }
  ]
  v(1cm)

  columns(2, doc)
}
