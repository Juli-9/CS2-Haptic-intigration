#import "thm-documentation.typ": *

#show: documentation.with(
  module: "Haptische Benutzerschnittstellen",
  term: "Sommersemester 2026",

  // Titel der Benutzerstudie eintragen
  title: "Hinweise zum Report in 'Haptische Benutzerschnittstellen'",

  // Namen und Matrikelnummern eintragen
  authors: (
    (
      name: "Prof. Dr. Martin Weigel",
      id: "-",
    ),
  ),
)

#let hl(t) = [
  #text(thm-green, t)
]

= Zusammenfassung
An erster Stelle im Dokument sollte eine Kurzzusammenfassung der Arbeit stehen. Üblicherweise beinhaltet die Zusammenfassung:
_Motivation_ des Themas (z.B. "Insbesondere im Sommer ist Flüssigkeitsmangel weit verbreitet und kann zu Kopfschmerzen, Konzentrationsschwäche und Schwindel führen."),
_Problem/Fragestellung_ ("Viele Menschen vergessen jedoch in ihrem Alltag ausreichend Trinkpausen einzulegen."),
_Lösungsansatz_ ("In dieser Arbeit präsentieren wir ein haptisches Armband namens HAPTrInK, welches den Benutzer in regelmäßigen Abständen an das Trinken erinnert."),
_Herangehensweise_ ("Das Armband überwacht die Umgebungstemperatur und errechnet den optimalen Trinkabstand. Der Benutzer bekommt ein Vibrationssignal, welches erst beendet wird wenn die IMU im Armband eine Trinkbewegung erkennt.") und das
_Hauptresultat_ ("Die Vibrationen am Handgelenk können gut im Alltag wahrgenommen werden, ohne zu viel Aufmerksamkeit von Dritten auf sich zu ziehen. Dadurch kann das Armband zu vielen Anlässen getragen werden und so zu mehr Flüssigkeitsaufnahme führen").
#text(thm-gray, "[~150 Wörter]")



= Einleitung
Als Teil der Prüfungsleistung von "II2521 Haptische Benutzerschnittstellen", soll eine Dokumentation zur Benutzerschnittstelle angefertigt werden. Dieses Dokument soll ihnen Hinweise und Ratschläge zur Struktur, Inhalten und Formulierungen geben.

Dokumentation kann in Deutsch oder Englisch geschrieben werden. Benutzen Sie als Vorlage diese Typst-Vorlage. Typst #cite(<typst>) ist eine relativ neue Alternative zu LaTeX. Die Verwendung anderer Programme (Word, LaTeX, usw.) ist möglich. In diesem Fall müssen Sie die Vorlage aber selbstständig nachbauen. Es gibt Punktabzüge, wenn die Dokumentation zu stark von dieser Vorlage abweicht. Den Titel können Sie frei wählen. Bei technischen Systemen setzt er sich meist aus dem Projektnamen und einer Kurzbeschreibung zusammen (z.B. "HAPTrInK: Trinkerinnerungen per Vibrationsarmband"). Wissenschaftliche Arbeiten benutzen übrigens häufig "we/wir", auch wenn es nur einen Autor gibt. Nutzen Sie in diesem Report aber gerne das Pronomen mit dem Sie sich am Besten fühlen. Insgesamt sollte ihre Dokumentation 4--6 Seiten umfassen. Exportieren Sie das Dokument vor der Einreichung als PDF und laden Sie es im Kurs-Moodle hoch.

Nachdem Sie die Kurzzusammenfassung bereits kennen gelernt haben, sind wir inzwischen im ersten Kapitel des Hauptdokuments angekommen. Die Einleitung wiederholt die Zusammenfassung und erweitert Sie mit Details (z.B. "Im Jahre 2020 gab es in Deutschland 108.000 Krankenhausbehandlungen wegen Flüssigkeitsmangel und 3.300 Todesfälle @aponet."). Die Projektidee sollte hergeleitet und erklärt werden (z.B. welchen Vorteil hat die Haptik im Vergleich zu visueller oder auditiver Ausgabe in dieser Anwendung?). Außerdem wird der Ansatz der Benutzerschnittstelle genauer vorgestellt und die Hauptkomponenten (Software, Hardware, APIs) schon einmal erwähnt.

Optional: Im Anschluss können Sie den Aufbau der Dokumentationskapitel erklären.



= (Optional) Beispielszenario
Manchmal hilft ein Beispielszenario, um den Nutzen von Benutzerschnittstellen zu erklären. Hier können Sie eine kurze Geschichte mit einer fiktionalen Person erzählen: "Alice soll einen Stand auf dem Sommerfest der Hochschule betreuen. Das Sommerfest hält was es verspricht und findet an einem sehr warmen Tag bei 36°C statt. Da Alice bereits letztes Jahr am Sommerfest teilgenommen hat, weiß sie dass man bei den vielen interessanten Gesprächen schnell vergessen kann ausreichend Flüssigkeit zu sich zu nehmen. Dieses Jahr hat sie sich daher ein HAPTrInK Armband gekauft. Während Alice sich auf die interessanten Unterhaltungen konzentriert, erinnert sie das Armband regelmäßig durch leichte Vibrationen daran etwas zu trinken. Daraufhin nimmt Alice ihre Trinkflasche und trinkt ein paar Schlucke. HAPTrInK erkennt die Trinkbewegung automatisch und stoppt die Vibration. Alice gefällt besonders, dass die Gesprächspartner von alldem nichts mitbekommen und der Unterhaltungsfluss nicht unterbrochen wird."



= (Optional) Forschungsstand
Falls Sie ähnliche Arbeiten zu ihrer Benutzerschnittstelle kennen (z.B. Lösungen für das gleiche Problem ohne Haptik, ähnliche tragbare Geräte für andere Anwendungen, usw.), können Sie diese hier benennen und referenzieren. Bei einer Abschluss- oder Forschungsarbeit ist dieses Kapitel sehr wichtig, da Sie hier zeigen müssen wie sich ihre Arbeit von themenverwandten Arbeiten abgrenzt. Die Referenzen können mit `#cite(<id>)` in Typst (`id` entspricht der Eintrags-ID in `references.bib`) oder manuell als [nummer] in Word gesetzt werden und sollten einen Verweis am Ende des Dokumentes unter _Bibliographie_ besitzen. Für den Kurs ist dieses Kapitel optional.



= HAPTrInK [bzw. ihr Projektname]
Dieses Kapitel enthält alle relevanten Informationen über HAPTrInK, das haptische Armband für Trinkerinnerungen.

#hl[
  Stilistisch sollte man vermeiden, dass zwei Überschriften direkt aufeinander folgen. Daher immer einen Überleitungssatz hinzufügen (z.B. worum es insgesamt im Kapitel geht).
]

== Systemübersicht
Hier sollten alle notwendigen Details für das System (Hardware + Software) erklärt werden.

Dieses Kapitel soll helfen das System und seine Komponenten zu verstehen. Beispielinhalte:
 - Wie genau sieht der Prototyp aus und wie wird er benutzt? Z.B. bei Wearables: Wie wird es am Körper befestigt? Abbildung mit einem Foto der haptischen Benutzerschnittstelle (am Besten während der Benutzung). Gerne auch mit Annotation der Komponenten.
 - Aus welchen Komponenten besteht das Gesamtsystem? Gibt es eine Computer-/Serveranwendung? Externe APIs? (Eventuell mit Systemübersichtsgrafik.)
 - Wie ist die Hardware zusammengesetzt? Wie kommunizieren die Komponenten miteinander (I2C, SPI, UART, o.ä.)? (Eventuell mit einem Schaltbild.)
 - Wie kommuniziert das Gerät mit der Außenwelt (serielle Schnittstelle? WLAN? Protokoll?)
 - Gibt es wichtige (nicht triviale) Algorithmen? Falls ja, können diese beschrieben werden oder als Appendix angehängt werden.
 - Welche externe Frameworks und Bibliotheken wurden verwendet (+ Version)?
 - Wichtige Details zum Gesamtsystem (z.B. Größe, Gewicht, Stromverbrauch, ...)

== Haptische Stimuli
Erklären Sie welche haptischen Signale von ihrem System benutzt werden, z.B.:

- Was für Aktuatoren? Wieviele? Wo am Körper sind diese platziert? Welche Überlegungen gab es bei der Platzierung? Falls es nicht aus der Systemabbildung ersichtlich ist, können Sie die Positionen auf einem Bild vom Körperteil einzeichnen.
- Wie wurden die Aktuatoren angesteuert? Welche Intensitäten und Signallängen wurden gewählt (und warum)?
- Wurden Effekte oder Optimierungen implementiert (z.B. Ramps oder ein Overdrive)?
- Wurden haptische Illusionen benutzt? Wie genau wurden diese Implementiert?
- Bei komplexen Signalen eventuell eine Grafik/ein Diagram benutzen. Häufig wird die Intensität auf der Y-Achse eingezeichnet und die Zeit auf der x-Achse.
- Werden die Signalstärken an den Benutzer angepasst oder kann der gleiche Stimuli verwendet werden?

#hl[
  Ihre Dokumentation sollte aus Fließtext bestehen. Die Stichpunkte aus diesem Dokument dienen nur, ihnen eine Übersicht über mögliche Themen zu geben.
]

== [Netzwerkkommunikation / API / Desktop-Anwendung / ...]
Falls Sie sehr viel Aufwand in eine bestimmte Komponente investiert haben, können Sie diese auch in einer eigenen Sektion beschreiben. Zum Beispiel, wie Sensorwerte ausgelesen und verarbeitet wurden. Oder wie im Detail die Kommunikation mit einer API aussah. Oder eine Sektion zu ihrer Desktop-/Web-/Mobilanwendung, welche erklärt wie sie diese implementiert haben. Wenn Sie ein eigenes Case erstellt haben (z.B. 3D Druck), geben Sie die Details an. Passen Sie die Struktur also gerne Ihren Anforderungen und Bedürfnissen an. Nutzen Sie die Chance in der Dokumentation (und Präsentation) sich von ihrer Besten Seite zu präsentieren und auf wichtige Leistungen hinzuweisen.



= Diskussion
- Wurden andere Haptische Stimuli implementiert und verglichen? Wieso wurde die oben gewählte implementierung gewählt? Dieses Kapitel gibt ihnen die Chance auch Dinge zu erwähnen, welche es nicht in die finale Version geschafft haben (z.B. weil sie einen besseren Weg gefunden haben).
- Was haben Sie über Haptik gelernt? Gab es Körperstellen welche nicht gut funktioniert haben? War das Empfinden zwischen Benutzern unterschiedlich?
- Erfüllt das System seinen Zweck? Was haben Sie über das Anwendungsgebiet dazugelernt?

#hl[
  Versuchen Sie bei der Diskussion objektiv zu bleiben. Da Sie keine formale Benutzerstudie gemacht haben, können Sie hier meist nur Vermutungen äußern (was ok und auch erwünscht ist).
]



= Limitierungen
Was sind Nachteile ihres Prototypens? Hier ein paar Ideen:
- Wo könnte es bei der Verwendung im angestrebten Szenario noch Probleme geben?
- Ist der Prototyp schon ausreichend benutzbar? Kann der Prototyp über eine (Web-)Schnittstelle konfiguriert werden oder muss für jede Änderung das Programm neu geflasht werden? Funktioniert die Anwendung immer oder nur in einem speziellen Szenario (z.B. ein bestimmter Ort oder innerhalb einer Anwendung).
- Sind die Probleme technisch zu lösen (falls ja gerne benennen wie) oder wäre ein Produkt (!= Prototyp) zur Zeit noch nicht machbar?

#hl[
  Innerhalb des Kurses bauen Sie einen Prototypen, kein Produkt. Prototypen haben üblicherweise sehr viele Limitierungen. Da Sie nicht alle aufzählen können, wählen Sie nur die Offensichtlichsten. Zum Einen diejenigen, von denen Sie wirklich erwarten, dass sie einen größeren Aufwand darstellen und diejenigen welche einem Leser am wahrscheinlichsten durch den Kopf gehen. Dadurch zeigen Sie, dass sie das Themenfeld und Projekt verstanden haben. Gerade im späteren Berufsleben ist dies wichtig, da Sie dort häufig mithilfe eines Prototypen neue Ideen testen und danach entscheiden müssen, ob es realistisch ist diese in ein Produkt zu verwandeln.
]

#hl[
    Das Kapitel _Limitierungen_ wird auch häufig mit der Diskussion zusammengelegt. Insbesondere wenn es viele Überschneidungen gibt _Diskussion und Limitierungen_.
]



= Fazit
Fassen Sie die Arbeit noch einmal kurz zusammen:
- Was für eine Benutzerschnittstelle wurde gebaut?
- Was für einen Zweck erfüllte die Benutzerschnittstelle?
- Was soll der Leser der Dokumentation mitnehmen?

#text(size: 0.8em, thm-gray)[
  PS: Dieses Dokument gibt Hinweise und Inspirationen zur Struktur, Inhalten und Formulierungen für typische Dokumentationen. Sie können gerne von dem Dokument abweichen, solange ihre Dokumentation klar verständlich bleibt. Bei Fragen zur Dokumentation ihres Projektes, helfe ich gerne. Schreiben Sie mir einfach eine E-Mail oder fragen mich während der Veranstaltung.

  PPS: Die Präsentation und Dokumentation zum Projekt überlappen sich. Nutzen Sie gerne die gleichen Abbildungen und Strukturen, um sich arbeit zu sparen.

  PPPS: Auch wenn Rechtschreibung und Formatierung nicht das primäre Bewertungskriterium darstellt, zählt beides in den Gesamteindruck hinein. Niemand liest gerne Texte mit vielen Fehlern und schwer verständlichen Sätzen. Falls Sie selbst Probleme damit haben, nutzen Sie Schreibhilfen (z.B. die Korrekturhilfen in Microsoft Word) und geben Sie ihre Arbeit vor der Abgabe einer befreundeten Person zum Korrekturlesen.
]

#bibliography("references.bib")
