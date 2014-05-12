Entwicklung
--------------------------------------------------------------------------------

Windows/Linux Kompatibilität
================================================================================


Bitte im header file nur den Methodenkopf schreiben, nicht MeineKlasse::MeineMethode() Das schluckt der gcc nicht.

Lokale Anpassungen
================================================================================

Es gibt eine Konfigurationsdatei config.xml.in in dem Verzeichnis. Während der CMAKE-Konfiguration werden dort Variablennamen eingesetzt und die Datei dann nach MSML_Alphabet/config.xml kopiert. Nach dem Einlesen des Alphabetes stehen dann die Variablen zu Verfügung.

Derzeit wird der Mechanismus genutzt um den Pfad für die C++-Operatoren und die Pyhton-Files zu setzen. Aber der Mechanismus funktioniert für alle Variablen, die auf die lokale Maschine angepasst werden müssen (z.B. Verzeichnisse, Ports etc.).

